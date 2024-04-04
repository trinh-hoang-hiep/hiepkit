class OneOnly:
    _singleton = None
    def __new__(cls, *args, **kwargs):
        if not cls._singleton:
            cls._singleton = super(OneOnly, cls
                ).__new__(cls, *args, **kwargs)
        return cls._singleton

o1 = OneOnly()
o2 = OneOnly()

print(o1 == o2)


# Module-level Variables As Alternative
# provide mechanism to get access to the "default singleton" value, while also allowing creation of other instances if needed
# not technically a singleton, but provides the most Pythonic solution for singleton-like behavior

# Use of module-level variable to enhance state pattern
# No wasting memory on new instances by reusing a single state object for each 



class FirstTag:
    def process(self, remaining_string, parser):
        i_start_tag = remaining_string.find('<')
        i_end_tag = remaining_string.find('>')
        tag_name = remaining_string[i_start_tag+1:i_end_tag]
        root = Node(tag_name)
        parser.root = parser.current_node = root 
        parser.state = child_node # single state object reused for this state
        return remaining_string[i_end_tag+1:]
    
class ChildNode:
    def process(self, remaining_string, parser):
        stripped = remaining_string.strip()
        
        if stripped.startswith("</"):
            parser.state = close_tag # single state object reused for this state
        elif stripped.startswith("<"):
            parser.state = open_tag # single state object reused for this state
        else:
            parser.state = text_node # single state object reused for this state
        return stripped
    
    