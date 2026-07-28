# nodes.py
# Nova Programming Language - AST Nodes

class ASTNode:
    def __init__(self, node_type):
        self.node_type = node_type
        self.children = []
        self.properties = {}
        self.style = {}
    
    def add_child(self, child):
        self.children.append(child)
    
    def set_property(self, key, value):
        self.properties[key] = value
    
    def set_style(self, key, value):
        self.style[key] = value


class PageNode(ASTNode):
    def __init__(self, name):
        super().__init__('Page')
        self.name = name
        self.title = name
        self.language = 'en'
        self.theme_color = '#ffffff'


class TitleNode(ASTNode):
    def __init__(self, text):
        super().__init__('Title')
        self.text = text


class TextNode(ASTNode):
    def __init__(self, content):
        super().__init__('Text')
        self.content = content


class HeadingNode(ASTNode):
    def __init__(self, content):
        super().__init__('Heading')
        self.content = content


class SubtitleNode(ASTNode):
    def __init__(self, content):
        super().__init__('Subtitle')
        self.content = content


class SmallNode(ASTNode):
    def __init__(self, content):
        super().__init__('Small')
        self.content = content


class QuoteNode(ASTNode):
    def __init__(self, content):
        super().__init__('Quote')
        self.content = content


class CodeNode(ASTNode):
    def __init__(self, content):
        super().__init__('Code')
        self.content = content


class LinkNode(ASTNode):
    def __init__(self, text, url):
        super().__init__('Link')
        self.text = text
        self.url = url


class LabelNode(ASTNode):
    def __init__(self, text):
        super().__init__('Label')
        self.text = text


class ButtonNode(ASTNode):
    def __init__(self, name):
        super().__init__('Button')
        self.name = name
        self.text = name


class NumberInputNode(ASTNode):
    def __init__(self, name):
        super().__init__('NumberInput')
        self.name = name
        self.value = 0


class InputNode(ASTNode):
    def __init__(self, name):
        super().__init__('Input')
        self.name = name
        self.value = ''
        self.placeholder = ''


class PasswordNode(ASTNode):
    def __init__(self, name):
        super().__init__('Password')
        self.name = name


class EmailNode(ASTNode):
    def __init__(self, name, value=''):
        super().__init__('Email')
        self.name = name
        self.value = value


class SearchNode(ASTNode):
    def __init__(self, name):
        super().__init__('Search')
        self.name = name


class TextareaNode(ASTNode):
    def __init__(self, name):
        super().__init__('Textarea')
        self.name = name
        self.value = ''
        self.rows = 4
        self.cols = 50


class CheckboxNode(ASTNode):
    def __init__(self, name):
        super().__init__('Checkbox')
        self.name = name
        self.checked = False
        self.label = ''


class RadioNode(ASTNode):
    def __init__(self, name, value):
        super().__init__('Radio')
        self.name = name
        self.value = value
        self.checked = False
        self.label = value


class DropdownNode(ASTNode):
    def __init__(self, name):
        super().__init__('Dropdown')
        self.name = name
        self.options = []
        self.selected = ''


class DateNode(ASTNode):
    def __init__(self, name):
        super().__init__('Date')
        self.name = name


class TimeNode(ASTNode):
    def __init__(self, name):
        super().__init__('Time')
        self.name = name


class ColourNode(ASTNode):
    def __init__(self, name):
        super().__init__('Colour')
        self.name = name
        self.value = '#000000'


class SliderNode(ASTNode):
    def __init__(self, name):
        super().__init__('Slider')
        self.name = name
        self.min = 0
        self.max = 100
        self.value = 50


class UploadNode(ASTNode):
    def __init__(self, name):
        super().__init__('Upload')
        self.name = name
        self.accept = '*'


# NEW NODES FOR ADDED FEATURES

class ImageNode(ASTNode):
    def __init__(self, src, alt=''):
        super().__init__('Image')
        self.src = src
        self.alt = alt


class VideoNode(ASTNode):
    def __init__(self, src):
        super().__init__('Video')
        self.src = src


class AudioNode(ASTNode):
    def __init__(self, src):
        super().__init__('Audio')
        self.src = src


class GalleryNode(ASTNode):
    def __init__(self):
        super().__init__('Gallery')
        self.images = []


class SlideshowNode(ASTNode):
    def __init__(self):
        super().__init__('Slideshow')
        self.images = []
        self.interval = 3000


class ContainerNode(ASTNode):
    def __init__(self):
        super().__init__('Container')


class CardNode(ASTNode):
    def __init__(self, title=''):
        super().__init__('Card')
        self.title = title


class SectionNode(ASTNode):
    def __init__(self, title=''):
        super().__init__('Section')
        self.title = title


class NavbarNode(ASTNode):
    def __init__(self):
        super().__init__('Navbar')
        self.items = []


class NavLinkNode(ASTNode):
    def __init__(self, text, url):
        super().__init__('NavLink')
        self.text = text
        self.url = url


class FooterNode(ASTNode):
    def __init__(self):
        super().__init__('Footer')


class SidebarNode(ASTNode):
    def __init__(self):
        super().__init__('Sidebar')


class RowNode(ASTNode):
    def __init__(self):
        super().__init__('Row')


class ColumnNode(ASTNode):
    def __init__(self):
        super().__init__('Column')


class GridNode(ASTNode):
    def __init__(self, columns=3):
        super().__init__('Grid')
        self.columns = columns


class TabsNode(ASTNode):
    def __init__(self):
        super().__init__('Tabs')
        self.tabs = []


class TabNode(ASTNode):
    def __init__(self, title):
        super().__init__('Tab')
        self.title = title


class PanelNode(ASTNode):
    def __init__(self, title=''):
        super().__init__('Panel')
        self.title = title


class GroupNode(ASTNode):
    def __init__(self):
        super().__init__('Group')


# Event and Control Nodes

class WhenNode(ASTNode):
    def __init__(self, element, event, actions):
        super().__init__('When')
        self.element = element
        self.event = event
        self.actions = actions


class IfNode(ASTNode):
    def __init__(self, condition, body):
        super().__init__('If')
        self.condition = condition
        self.body = body
        self.else_body = None
        self.elif_conditions = []  # List of (condition, body) tuples


class ElifNode(ASTNode):
    def __init__(self, condition, body):
        super().__init__('Elif')
        self.condition = condition
        self.body = body


class OtherwiseNode(ASTNode):
    def __init__(self, body):
        super().__init__('Otherwise')
        self.body = body


class RepeatNode(ASTNode):
    def __init__(self, count, body):
        super().__init__('Repeat')
        self.count = count
        self.body = body


class RepeatWhileNode(ASTNode):
    def __init__(self, condition, body):
        super().__init__('RepeatWhile')
        self.condition = condition
        self.body = body


class ForEachNode(ASTNode):
    def __init__(self, item, list_name, body):
        super().__init__('ForEach')
        self.item = item
        self.list_name = list_name
        self.body = body


class StopNode(ASTNode):
    def __init__(self):
        super().__init__('Stop')


class ContinueNode(ASTNode):
    def __init__(self):
        super().__init__('Continue')


class BackgroundNode(ASTNode):
    def __init__(self, color):
        super().__init__('Background')
        self.color = color


class PopupNode(ASTNode):
    def __init__(self, message):
        super().__init__('Popup')
        self.message = message


class ConfirmNode(ASTNode):
    def __init__(self, message):
        super().__init__('Confirm')
        self.message = message


class AskUserNode(ASTNode):
    def __init__(self, message):
        super().__init__('AskUser')
        self.message = message


class NotificationNode(ASTNode):
    def __init__(self, message, duration=3000):
        super().__init__('Notification')
        self.message = message
        self.duration = duration


class ToastNode(ASTNode):
    def __init__(self, message):
        super().__init__('Toast')
        self.message = message


class AssignmentNode(ASTNode):
    def __init__(self, variable, value):
        super().__init__('Assignment')
        self.variable = variable
        self.value = value


class MakeListNode(ASTNode):
    def __init__(self, name):
        super().__init__('MakeList')
        self.name = name
        self.items = []


class AddItemNode(ASTNode):
    def __init__(self, list_name, item):
        super().__init__('AddItem')
        self.list_name = list_name
        self.item = item


class RemoveItemNode(ASTNode):
    def __init__(self, list_name, index):
        super().__init__('RemoveItem')
        self.list_name = list_name
        self.index = index


class InsertItemNode(ASTNode):
    def __init__(self, list_name, index, item):
        super().__init__('InsertItem')
        self.list_name = list_name
        self.index = index
        self.item = item


class SortNode(ASTNode):
    def __init__(self, list_name):
        super().__init__('Sort')
        self.list_name = list_name


class ReverseNode(ASTNode):
    def __init__(self, list_name):
        super().__init__('Reverse')
        self.list_name = list_name


class ShuffleNode(ASTNode):
    def __init__(self, list_name):
        super().__init__('Shuffle')
        self.list_name = list_name


class ListLengthNode(ASTNode):
    def __init__(self, list_name):
        super().__init__('ListLength')
        self.list_name = list_name


class ContainsItemNode(ASTNode):
    def __init__(self, list_name, item):
        super().__init__('ContainsItem')
        self.list_name = list_name
        self.item = item


class ValueNode(ASTNode):
    def __init__(self, token):
        super().__init__('Value')
        self.token = token
        self.value = token.value


class BinaryOpNode(ASTNode):
    def __init__(self, left, operator, right):
        super().__init__('BinaryOp')
        self.left = left
        self.operator = operator
        self.right = right


# Styling Node
class StyleNode(ASTNode):
    def __init__(self):
        super().__init__('Style')
        self.styles = {}

    def add_style(self, key, value):
        self.styles[key] = value


# Position Node
class PositionNode(ASTNode):
    def __init__(self, x, y, element=''):
        super().__init__('Position')
        self.x = x
        self.y = y
        self.element = element


# Function/Component Nodes
class ActionNode(ASTNode):
    def __init__(self, name, params=None, body=None):
        super().__init__('Action')
        self.name = name
        self.params = params or []
        self.body = body or []


class RunNode(ASTNode):
    def __init__(self, name, args=None):
        super().__init__('Run')
        self.name = name
        self.args = args or []


class ReturnNode(ASTNode):
    def __init__(self, value):
        super().__init__('Return')
        self.value = value


class ComponentNode(ASTNode):
    def __init__(self, name, body=None):
        super().__init__('Component')
        self.name = name
        self.body = body or []


class UseNode(ASTNode):
    def __init__(self, name):
        super().__init__('Use')
        self.name = name


class StateNode(ASTNode):
    def __init__(self, name, initial_value):
        super().__init__('State')
        self.name = name
        self.initial_value = initial_value


# Database/Storage Nodes
class ConnectDatabaseNode(ASTNode):
    def __init__(self, connection_string):
        super().__init__('ConnectDatabase')
        self.connection_string = connection_string


class SaveDatabaseNode(ASTNode):
    def __init__(self, collection, data):
        super().__init__('SaveDatabase')
        self.collection = collection
        self.data = data


class LoadDatabaseNode(ASTNode):
    def __init__(self, collection, query):
        super().__init__('LoadDatabase')
        self.collection = collection
        self.query = query


class UpdateDatabaseNode(ASTNode):
    def __init__(self, collection, query, data):
        super().__init__('UpdateDatabase')
        self.collection = collection
        self.query = query
        self.data = data


class DeleteDatabaseNode(ASTNode):
    def __init__(self, collection, query):
        super().__init__('DeleteDatabase')
        self.collection = collection
        self.query = query


# Auth Nodes
class LoginNode(ASTNode):
    def __init__(self, username, password):
        super().__init__('Login')
        self.username = username
        self.password = password


class LogoutNode(ASTNode):
    def __init__(self):
        super().__init__('Logout')


class SignupNode(ASTNode):
    def __init__(self, username, password, email):
        super().__init__('Signup')
        self.username = username
        self.password = password
        self.email = email


class EncryptNode(ASTNode):
    def __init__(self, data):
        super().__init__('Encrypt')
        self.data = data


class DecryptNode(ASTNode):
    def __init__(self, data):
        super().__init__('Decrypt')
        self.data = data


class HashNode(ASTNode):
    def __init__(self, data):
        super().__init__('Hash')
        self.data = data


class VerifyPasswordNode(ASTNode):
    def __init__(self, password, hash_value):
        super().__init__('VerifyPassword')
        self.password = password
        self.hash_value = hash_value


class GenerateTokenNode(ASTNode):
    def __init__(self):
        super().__init__('GenerateToken')


# Media Nodes
class CameraNode(ASTNode):
    def __init__(self):
        super().__init__('Camera')


class TakePhotoNode(ASTNode):
    def __init__(self):
        super().__init__('TakePhoto')


class RecordVideoNode(ASTNode):
    def __init__(self):
        super().__init__('RecordVideo')


class MicrophoneNode(ASTNode):
    def __init__(self):
        super().__init__('Microphone')


class RecordAudioNode(ASTNode):
    def __init__(self):
        super().__init__('RecordAudio')


# State Management Nodes
class ShowNode(ASTNode):
    def __init__(self, element):
        super().__init__('Show')
        self.element = element


class HideNode(ASTNode):
    def __init__(self, element):
        super().__init__('Hide')
        self.element = element


class EnableNode(ASTNode):
    def __init__(self, element):
        super().__init__('Enable')
        self.element = element


class DisableNode(ASTNode):
    def __init__(self, element):
        super().__init__('Disable')
        self.element = element


# Animation Nodes
class FadeInNode(ASTNode):
    def __init__(self, element, duration=1000):
        super().__init__('FadeIn')
        self.element = element
        self.duration = duration


class FadeOutNode(ASTNode):
    def __init__(self, element, duration=1000):
        super().__init__('FadeOut')
        self.element = element
        self.duration = duration


class SlideNode(ASTNode):
    def __init__(self, element, direction, distance=100):
        super().__init__('Slide')
        self.element = element
        self.direction = direction
        self.distance = distance


class GrowNode(ASTNode):
    def __init__(self, element, scale=1.5):
        super().__init__('Grow')
        self.element = element
        self.scale = scale


class ShrinkNode(ASTNode):
    def __init__(self, element, scale=0.5):
        super().__init__('Shrink')
        self.element = element
        self.scale = scale


class RotateNode(ASTNode):
    def __init__(self, element, degrees=180):
        super().__init__('Rotate')
        self.element = element
        self.degrees = degrees


class BounceNode(ASTNode):
    def __init__(self, element):
        super().__init__('Bounce')
        self.element = element


class SpinNode(ASTNode):
    def __init__(self, element):
        super().__init__('Spin')
        self.element = element


class ShakeNode(ASTNode):
    def __init__(self, element):
        super().__init__('Shake')
        self.element = element


class MoveToNode(ASTNode):
    def __init__(self, element, x, y):
        super().__init__('MoveTo')
        self.element = element
        self.x = x
        self.y = y


class MoveByNode(ASTNode):
    def __init__(self, element, dx, dy):
        super().__init__('MoveBy')
        self.element = element
        self.dx = dx
        self.dy = dy


class FlipHorizontalNode(ASTNode):
    def __init__(self, element):
        super().__init__('FlipHorizontal')
        self.element = element


class FlipVerticalNode(ASTNode):
    def __init__(self, element):
        super().__init__('FlipVertical')
        self.element = element


class AnimateNode(ASTNode):
    def __init__(self, element, animation, duration=500):
        super().__init__('Animate')
        self.element = element
        self.animation = animation
        self.duration = duration


# Progress/Loading Nodes
class ProgressNode(ASTNode):
    def __init__(self, value):
        super().__init__('Progress')
        self.value = value


class LoadingNode(ASTNode):
    def __init__(self):
        super().__init__('Loading')


# Storage Nodes
class SessionSaveNode(ASTNode):
    def __init__(self, key, value):
        super().__init__('SessionSave')
        self.key = key
        self.value = value


class CookieNode(ASTNode):
    def __init__(self, key, value):
        super().__init__('Cookie')
        self.key = key
        self.value = value


# HTTP Request Nodes
class PutToServerNode(ASTNode):
    def __init__(self, url, data):
        super().__init__('PutToServer')
        self.url = url
        self.data = data


class DeleteFromServerNode(ASTNode):
    def __init__(self, url):
        super().__init__('DeleteFromServer')
        self.url = url


class FetchNode(ASTNode):
    def __init__(self, url):
        super().__init__('Fetch')
        self.url = url


# File Operation Nodes
class SaveFileNode(ASTNode):
    def __init__(self, content, filename):
        super().__init__('SaveFile')
        self.content = content
        self.filename = filename


class OpenFileNode(ASTNode):
    def __init__(self, filename):
        super().__init__('OpenFile')
        self.filename = filename


class DeleteFileNode(ASTNode):
    def __init__(self, filename):
        super().__init__('DeleteFile')
        self.filename = filename


class RenameFileNode(ASTNode):
    def __init__(self, old_name, new_name):
        super().__init__('RenameFile')
        self.old_name = old_name
        self.new_name = new_name


# Web Navigation Nodes
class OpenWebsiteNode(ASTNode):
    def __init__(self, url):
        super().__init__('OpenWebsite')
        self.url = url


class SharePageNode(ASTNode):
    def __init__(self):
        super().__init__('SharePage')


class CopyLinkNode(ASTNode):
    def __init__(self):
        super().__init__('CopyLink')


# Media Control Nodes
class StopMediaNode(ASTNode):
    def __init__(self, element):
        super().__init__('StopMedia')
        self.element = element


class PrintPageNode(ASTNode):
    def __init__(self):
        super().__init__('PrintPage')


# Mathematical Operation Nodes
class PowerNode(ASTNode):
    def __init__(self, base, exponent):
        super().__init__('Power')
        self.base = base
        self.exponent = exponent


class SquareRootNode(ASTNode):
    def __init__(self, value):
        super().__init__('SquareRoot')
        self.value = value


class AbsoluteNode(ASTNode):
    def __init__(self, value):
        super().__init__('Absolute')
        self.value = value


class FloorNode(ASTNode):
    def __init__(self, value):
        super().__init__('Floor')
        self.value = value


class CeilingNode(ASTNode):
    def __init__(self, value):
        super().__init__('Ceiling')
        self.value = value


class ModNode(ASTNode):
    def __init__(self, left, right):
        super().__init__('Mod')
        self.left = left
        self.right = right


# String Operation Nodes
class UppercaseNode(ASTNode):
    def __init__(self, value):
        super().__init__('Uppercase')
        self.value = value


class LowercaseNode(ASTNode):
    def __init__(self, value):
        super().__init__('Lowercase')
        self.value = value


class CapitalizeNode(ASTNode):
    def __init__(self, value):
        super().__init__('Capitalize')
        self.value = value


class TrimNode(ASTNode):
    def __init__(self, value):
        super().__init__('Trim')
        self.value = value


class ReplaceNode(ASTNode):
    def __init__(self, string, old, new):
        super().__init__('Replace')
        self.string = string
        self.old = old
        self.new = new


class ContainsNode(ASTNode):
    def __init__(self, string, substring):
        super().__init__('Contains')
        self.string = string
        self.substring = substring


class StartsWithNode(ASTNode):
    def __init__(self, string, prefix):
        super().__init__('StartsWith')
        self.string = string
        self.prefix = prefix


class EndsWithNode(ASTNode):
    def __init__(self, string, suffix):
        super().__init__('EndsWith')
        self.string = string
        self.suffix = suffix


class LengthOfNode(ASTNode):
    def __init__(self, value):
        super().__init__('LengthOf')
        self.value = value

# nodes.py - Add server nodes

class RouteNode(ASTNode):
    """HTTP Route Node"""
    def __init__(self, path, method, body):
        super().__init__('Route')
        self.path = path
        self.method = method
        self.body = body