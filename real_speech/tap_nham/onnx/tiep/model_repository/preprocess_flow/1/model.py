# Copyright (c) 2023, NVIDIA CORPORATION. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#  * Neither the name of NVIDIA CORPORATION nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE.
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import numpy as np
import sys
import json
import io
import math
# triton_python_backend_utils is available in every Triton Python model. You
# need to use this module to create inference requests and responses. It also
# contains some utility functions for extracting information from model_config
# and converting Triton input/output types to numpy types.
import triton_python_backend_utils as pb_utils
# import cv2
import os
import torch
from torch.nn import functional as F


class TritonPythonModel:
    """Your Python model must use the same class name. Every Python model
    that is created must have "TritonPythonModel" as the class name.
    """

    def initialize(self, args):
        """`initialize` is called only once when the model is being loaded.
        Implementing `initialize` function is optional. This function allows
        the model to intialize any state associated with this model.
        Parameters
        ----------
        args : dict
          Both keys and values are strings. The dictionary keys and values are:
          * model_config: A JSON string containing the model configuration
          * model_instance_kind: A string containing model instance kind
          * model_instance_device_id: A string containing model instance device ID
          * model_repository: Model repository path
          * model_version: Model version
          * model_name: Model name
        """

        # You must parse model_config. JSON string is not parsed here
        model_config = json.loads(args['model_config'])

        # Get OUTPUT0 configuration
        output1_config = pb_utils.get_output_config_by_name(
            model_config, "preprocess_flow_output_1")
        
        output2_config = pb_utils.get_output_config_by_name(
            model_config, "preprocess_flow_output_2")
        

        # Convert Triton types to numpy types
        self.output1_dtype = pb_utils.triton_string_to_numpy(
            output1_config['data_type'])
        
        self.output2_dtype = pb_utils.triton_string_to_numpy(
            output2_config['data_type'])
        
    def execute(self, requests):
        """`execute` MUST be implemented in every Python model. `execute`
        function receives a list of pb_utils.InferenceRequest as the only
        argument. This function is called when an inference request is made
        for this model. Depending on the batching configuration (e.g. Dynamic
        Batching) used, `requests` may contain multiple requests. Every
        Python model, must create one pb_utils.InferenceResponse for every
        pb_utils.InferenceRequest in `requests`. If there is an error, you can
        set the error argument when creating a pb_utils.InferenceResponse
        Parameters
        ----------
        requests : list
          A list of pb_utils.InferenceRequest
        Returns
        -------
        list
          A list of pb_utils.InferenceResponse. The length of this list must
          be the same as `requests`
        """

        output1_dtype = self.output1_dtype
        output2_dtype = self.output2_dtype
        print(f"preprocess flow !!!!!!!!!!!!!!!!!!")
        responses = []
        def convert_pad_shape(pad_shape):
            l = pad_shape[::-1]
            pad_shape = [item for sublist in l for item in sublist]
            return pad_shape
        
        def sequence_mask(length, max_length=None):
            if max_length is None:
                max_length = length.max()
            x = torch.arange(max_length, dtype=length.dtype, device=length.device)
            return x.unsqueeze(0) < length.unsqueeze(1)
        
        def generate_path(duration, mask):
            """
            duration: [b, 1, t_x]
            mask: [b, 1, t_y, t_x]
            """
            
            b, _, t_y, t_x = mask.shape
            cum_duration = torch.cumsum(duration, -1)
            
            cum_duration_flat = cum_duration.view(b * t_x)
            path = sequence_mask(cum_duration_flat, t_y).to(mask.dtype)
            path = path.view(b, t_x, t_y)
            path = path - F.pad(path, convert_pad_shape([[0, 0], [1, 0], [0, 0]]))[:, :-1]
            path = path.unsqueeze(1).transpose(2,3) * mask
            return path


        # Every Python backend must iterate over everyone of the requests
        # and create a pb_utils.InferenceResponse for each of them.
        for request in requests:
            # Get INPUT0
            in_1 = pb_utils.get_input_tensor_by_name(request, "preprocess_flow_input_1").as_numpy()
            in_2 = pb_utils.get_input_tensor_by_name(request, "preprocess_flow_input_2").as_numpy()
            in_3 = pb_utils.get_input_tensor_by_name(request, "preprocess_flow_input_3").as_numpy()
            in_4 = pb_utils.get_input_tensor_by_name(request, "preprocess_flow_input_4").as_numpy()
            
            length_scale = 1
            noise_scale=.667
            
            in_1 = torch.from_numpy(in_1)
            
            in_2 = torch.from_numpy(in_2)
            in_3 = torch.from_numpy(in_3)
            in_4 = torch.from_numpy(in_4)
            w = torch.exp(in_2) * in_1 * length_scale
            w_ceil = torch.ceil(w)
            y_lengths = torch.clamp_min(torch.sum(w_ceil, [1, 2]), 1).long()
            y_mask = torch.unsqueeze(sequence_mask(y_lengths, None), 1).to(in_1.dtype)
            attn_mask = torch.unsqueeze(in_1, 2) * torch.unsqueeze(y_mask, -1)
            attn = generate_path(w_ceil, attn_mask)
            
            in_3 = torch.matmul(attn.squeeze(1), in_3.transpose(1, 2)).transpose(1, 2) # [b, t', t], [b, t, d] -> [b, d, t']
            in_4 = torch.matmul(attn.squeeze(1), in_4.transpose(1, 2)).transpose(1, 2) # [b, t', t], [b, t, d] -> [b, d, t']
            
            z_p = in_3 + torch.randn_like(in_3) * torch.exp(in_4) * noise_scale
            z_p = z_p.numpy().astype(np.float32)
            
            y_mask = y_mask.numpy().astype(np.float32)
            
            print(f"z_p.shape: {z_p.shape}")
            print(f"y_mask.shape: {y_mask.shape}")

            
            out_tensor_1 = pb_utils.Tensor("preprocess_flow_output_1",
                                           z_p.astype(output1_dtype))
            
            out_tensor_2 = pb_utils.Tensor("preprocess_flow_output_2",
                                           y_mask.astype(output2_dtype))
            

            inference_response = pb_utils.InferenceResponse(
                output_tensors=[out_tensor_1,out_tensor_2])
            responses.append(inference_response)
        # You should return a list of pb_utils.InferenceResponse. Length
        # of this list must match the length of `requests` list.
        return responses

    def finalize(self):
        """`finalize` is called only once when the model is being unloaded.
        Implementing `finalize` function is OPTIONAL. This function allows
        the model to perform any necessary clean ups before exit.
        """
        print('Cleaning up...')

