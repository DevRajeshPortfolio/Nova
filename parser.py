# parser.py
# Nova Programming Language - Parser

from tokens import *
from nodes import *
from errors import *


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_idx = 0
        self.current_token = tokens[0] if tokens else None
        self.ast = []
        self.errors = []
    
    def advance(self):
        self.token_idx += 1
        if self.token_idx < len(self.tokens):
            self.current_token = self.tokens[self.token_idx]
        else:
            self.current_token = None
    
    def parse(self):
        """Parse the entire token stream"""
        while self.current_token and self.current_token.type != TT_EOF:
            node = self.parse_statement()
            if node:
                self.ast.append(node)
            else:
                # Skip unknown tokens
                self.advance()
        return self.ast
    
    def parse_statement(self):
        """Parse a single statement"""
        token = self.current_token
        
        if token is None:
            return None
            
        if token.type == TT_KEYWORD:
            if token.value == 'page':
                return self.parse_page()
            elif token.value == 'button':
                return self.parse_button()
            elif token.value == 'number':
                return self.parse_number_input()
            elif token.value == 'text':
                return self.parse_text()
            elif token.value == 'heading':
                return self.parse_heading()
            elif token.value == 'subtitle':
                return self.parse_subtitle()
            elif token.value == 'small':
                return self.parse_small()
            elif token.value == 'quote':
                return self.parse_quote()
            elif token.value == 'code':
                return self.parse_code()
            elif token.value == 'link':
                return self.parse_link()
            elif token.value == 'label':
                return self.parse_label()
            elif token.value == 'input':
                return self.parse_input()
            elif token.value == 'password':
                return self.parse_password()
            elif token.value == 'email':
                return self.parse_email()
            elif token.value == 'search':
                return self.parse_search()
            elif token.value == 'textarea':
                return self.parse_textarea()
            elif token.value == 'checkbox':
                return self.parse_checkbox()
            elif token.value == 'radio':
                return self.parse_radio()
            elif token.value == 'dropdown':
                return self.parse_dropdown()
            elif token.value == 'date':
                return self.parse_date()
            elif token.value == 'time':
                return self.parse_time()
            elif token.value == 'colour':
                return self.parse_colour()
            elif token.value == 'slider':
                return self.parse_slider()
            elif token.value == 'upload':
                return self.parse_upload()
            elif token.value == 'title':
                return self.parse_title()
            elif token.value == 'when':
                return self.parse_when()
            elif token.value == 'popup':
                return self.parse_popup()
            elif token.value == 'if':
                return self.parse_if()
            elif token.value == 'elif':
                return self.parse_elif()
            elif token.value == 'otherwise':
                return self.parse_otherwise()
            elif token.value == 'background':
                return self.parse_background()
            # NEW KEYWORDS
            elif token.value == 'image':
                return self.parse_image()
            elif token.value == 'video':
                return self.parse_video()
            elif token.value == 'audio':
                return self.parse_audio()
            elif token.value == 'gallery':
                return self.parse_gallery()
            elif token.value == 'slideshow':
                return self.parse_slideshow()
            elif token.value == 'container':
                return self.parse_container()
            elif token.value == 'card':
                return self.parse_card()
            elif token.value == 'section':
                return self.parse_section()
            elif token.value == 'navbar':
                return self.parse_navbar()
            elif token.value == 'footer':
                return self.parse_footer()
            elif token.value == 'sidebar':
                return self.parse_sidebar()
            elif token.value == 'row':
                return self.parse_row()
            elif token.value == 'column':
                return self.parse_column()
            elif token.value == 'grid':
                return self.parse_grid()
            elif token.value == 'tabs':
                return self.parse_tabs()
            elif token.value == 'panel':
                return self.parse_panel()
            elif token.value == 'group':
                return self.parse_group()
            elif token.value == 'position':
                return self.parse_position()
            # NEW EVENT KEYWORDS
            elif token.value == 'whenblurred':
                return self.parse_when_blurred()
            elif token.value == 'whenpageopens':
                return self.parse_when_page_opens()
            elif token.value == 'whenpagecloses':
                return self.parse_when_page_closes()
            elif token.value == 'whenscrolled':
                return self.parse_when_scrolled()
            # NEW LOOP KEYWORDS
            elif token.value == 'repeat':
                return self.parse_repeat()
            elif token.value == 'repeatwhile':
                return self.parse_repeat_while()
            elif token.value == 'for':
                return self.parse_for_each()
            elif token.value == 'stop':
                return self.parse_stop()
            elif token.value == 'continue':
                return self.parse_continue()
            # NEW MATH OPERATIONS
            elif token.value == 'power':
                return self.parse_power()
            elif token.value == 'squareroot':
                return self.parse_squareroot()
            elif token.value == 'absolute':
                return self.parse_absolute()
            elif token.value == 'floor':
                return self.parse_floor()
            elif token.value == 'ceiling':
                return self.parse_ceiling()
            elif token.value == 'mod':
                return self.parse_mod()
            # NEW STRING OPERATIONS
            elif token.value == 'uppercase':
                return self.parse_uppercase()
            elif token.value == 'lowercase':
                return self.parse_lowercase()
            elif token.value == 'capitalize':
                return self.parse_capitalize()
            elif token.value == 'trim':
                return self.parse_trim()
            elif token.value == 'replace':
                return self.parse_replace()
            elif token.value == 'contains':
                return self.parse_contains()
            elif token.value == 'startswith':
                return self.parse_startswith()
            elif token.value == 'endswith':
                return self.parse_endswith()
            elif token.value == 'lengthof':
                return self.parse_lengthof()
            # NEW LIST OPERATIONS
            elif token.value == 'makelist':
                return self.parse_makelist()
            elif token.value == 'additem':
                return self.parse_additem()
            elif token.value == 'removeitem':
                return self.parse_removeitem()
            elif token.value == 'insertitem':
                return self.parse_insertitem()
            elif token.value == 'sort':
                return self.parse_sort()
            elif token.value == 'reverse':
                return self.parse_reverse()
            elif token.value == 'shuffle':
                return self.parse_shuffle()
            elif token.value == 'listlength':
                return self.parse_listlength()
            elif token.value == 'containsitem':
                return self.parse_containsitem()
            # NEW STORAGE KEYWORDS
            elif token.value == 'sessionsave':
                return self.parse_sessionsave()
            elif token.value == 'cookie':
                return self.parse_cookie()
            # NEW DATABASE KEYWORDS
            elif token.value == 'connectdatabase':
                return self.parse_connectdatabase()
            elif token.value == 'savedatabase':
                return self.parse_savedatabase()
            elif token.value == 'loaddatabase':
                return self.parse_loaddatabase()
            elif token.value == 'updatedatabase':
                return self.parse_updatedatabase()
            elif token.value == 'deletedatabase':
                return self.parse_deletedatabase()
            # NEW AUTH KEYWORDS
            elif token.value == 'login':
                return self.parse_login()
            elif token.value == 'logout':
                return self.parse_logout()
            elif token.value == 'signup':
                return self.parse_signup()
            elif token.value == 'encrypt':
                return self.parse_encrypt()
            elif token.value == 'decrypt':
                return self.parse_decrypt()
            elif token.value == 'hash':
                return self.parse_hash()
            elif token.value == 'verifypassword':
                return self.parse_verifypassword()
            elif token.value == 'generatetoken':
                return self.parse_generatetoken()
            # NEW UI KEYWORDS
            elif token.value == 'confirm':
                return self.parse_confirm()
            elif token.value == 'askuser':
                return self.parse_askuser()
            elif token.value == 'notification':
                return self.parse_notification()
            elif token.value == 'toast':
                return self.parse_toast()
            elif token.value == 'progress':
                return self.parse_progress()
            elif token.value == 'loading':
                return self.parse_loading()
            # NEW STATE KEYWORDS
            elif token.value == 'show':
                return self.parse_show()
            elif token.value == 'hide':
                return self.parse_hide()
            elif token.value == 'enable':
                return self.parse_enable()
            elif token.value == 'disable':
                return self.parse_disable()
            # NEW ANIMATION KEYWORDS
            elif token.value == 'fadein':
                return self.parse_fadein()
            elif token.value == 'fadeout':
                return self.parse_fadeout()
            elif token.value == 'slide':
                return self.parse_slide()
            elif token.value == 'grow':
                return self.parse_grow()
            elif token.value == 'shrink':
                return self.parse_shrink()
            elif token.value == 'rotate':
                return self.parse_rotate()
            elif token.value == 'bounce':
                return self.parse_bounce()
            elif token.value == 'spin':
                return self.parse_spin()
            elif token.value == 'shake':
                return self.parse_shake()
            elif token.value == 'moveto':
                return self.parse_moveto()
            elif token.value == 'moveby':
                return self.parse_moveby()
            elif token.value == 'fliphorizontal':
                return self.parse_fliphorizontal()
            elif token.value == 'flipvertical':
                return self.parse_flipvertical()
            elif token.value == 'animate':
                return self.parse_animate()
            # NEW WEB NAVIGATION
            elif token.value == 'openwebsite':
                return self.parse_openwebsite()
            elif token.value == 'sharepage':
                return self.parse_sharepage()
            elif token.value == 'copylink':
                return self.parse_copylink()
            elif token.value == 'printpage':
                return self.parse_printpage()
            # NEW FILE OPERATIONS
            elif token.value == 'savefile':
                return self.parse_savefile()
            elif token.value == 'openfile':
                return self.parse_openfile()
            elif token.value == 'deletefile':
                return self.parse_deletefile()
            elif token.value == 'renamefile':
                return self.parse_renamefile()
            # NEW MEDIA OPERATIONS
            elif token.value == 'stop':
                return self.parse_stop_media()
            elif token.value == 'camera':
                return self.parse_camera()
            elif token.value == 'takephoto':
                return self.parse_takephoto()
            elif token.value == 'recordvideo':
                return self.parse_recordvideo()
            elif token.value == 'microphone':
                return self.parse_microphone()
            elif token.value == 'recordaudio':
                return self.parse_recordaudio()
            # NEW ACTION/FUNCTION KEYWORDS
            elif token.value == 'action':
                return self.parse_action()
            elif token.value == 'run':
                return self.parse_run()
            elif token.value == 'return':
                return self.parse_return()
            elif token.value == 'component':
                return self.parse_component()
            elif token.value == 'use':
                return self.parse_use()
            elif token.value == 'state':
                return self.parse_state()
            # NEW HTTP REQUEST KEYWORDS
            elif token.value == 'puttoserver':
                return self.parse_puttoserver()
            elif token.value == 'deletefromserver':
                return self.parse_deletefromserver()
            elif token.value == 'fetch':
                return self.parse_fetch()
            # STYLING KEYWORDS (these are handled within nodes)
            elif token.value in ['textcolour', 'bordercolour', 'hovercolour', 'pressedcolour', 
                                 'transparent', 'gradient', 'font', 'textsize', 'bold', 'italic',
                                 'underline', 'align', 'width', 'height', 'padding', 'margin',
                                 'border', 'roundcorners', 'shadow', 'opacity', 'blur',
                                 'center', 'left', 'right', 'top', 'bottom']:
                # These are handled in parse_style_attributes
                return self.parse_style_attribute(token.value)
            else:
                self.advance()
                return None
        elif token.type == TT_IDENTIFIER:
            return self.parse_assignment()
        else:
            self.advance()
            return None
    
    # ... (keep all existing parsing methods)

    # NEW PARSER METHODS
    
    # Events
    def parse_when_blurred(self):
        """Parse when blurred event"""
        self.advance()  # Skip 'whenblurred'
        
        if self.current_token and self.current_token.type == TT_IDENTIFIER:
            element = self.current_token.value
            self.advance()  # Skip element name
            
            # Check for newline and indent
            if self.current_token and self.current_token.type == TT_NEWLINE:
                self.advance()
            
            if self.current_token and self.current_token.type == TT_INDENT:
                self.advance()  # Skip INDENT
                
                actions = []
                while self.current_token and self.current_token.type != TT_DEDENT and self.current_token.type != TT_EOF:
                    action = self.parse_statement()
                    if action:
                        actions.append(action)
                    else:
                        self.advance()
                
                if self.current_token and self.current_token.type == TT_DEDENT:
                    self.advance()  # Skip DEDENT
                
                return WhenNode(element, 'blur', actions)
        
        return None
    
    def parse_when_page_opens(self):
        """Parse when page opens event"""
        self.advance()  # Skip 'whenpageopens'
        
        # Check for newline and indent
        if self.current_token and self.current_token.type == TT_NEWLINE:
            self.advance()
        
        if self.current_token and self.current_token.type == TT_INDENT:
            self.advance()  # Skip INDENT
            
            actions = []
            while self.current_token and self.current_token.type != TT_DEDENT and self.current_token.type != TT_EOF:
                action = self.parse_statement()
                if action:
                    actions.append(action)
                else:
                    self.advance()
            
            if self.current_token and self.current_token.type == TT_DEDENT:
                self.advance()  # Skip DEDENT
            
            return WhenNode('document', 'DOMContentLoaded', actions)
        
        return None
    
    def parse_when_page_closes(self):
        """Parse when page closes event"""
        self.advance()  # Skip 'whenpagecloses'
        
        # Check for newline and indent
        if self.current_token and self.current_token.type == TT_NEWLINE:
            self.advance()
        
        if self.current_token and self.current_token.type == TT_INDENT:
            self.advance()  # Skip INDENT
            
            actions = []
            while self.current_token and self.current_token.type != TT_DEDENT and self.current_token.type != TT_EOF:
                action = self.parse_statement()
                if action:
                    actions.append(action)
                else:
                    self.advance()
            
            if self.current_token and self.current_token.type == TT_DEDENT:
                self.advance()  # Skip DEDENT
            
            return WhenNode('document', 'beforeunload', actions)
        
        return None
    
    def parse_when_scrolled(self):
        """Parse when scrolled event"""
        self.advance()  # Skip 'whenscrolled'
        
        # Check for newline and indent
        if self.current_token and self.current_token.type == TT_NEWLINE:
            self.advance()
        
        if self.current_token and self.current_token.type == TT_INDENT:
            self.advance()  # Skip INDENT
            
            actions = []
            while self.current_token and self.current_token.type != TT_DEDENT and self.current_token.type != TT_EOF:
                action = self.parse_statement()
                if action:
                    actions.append(action)
                else:
                    self.advance()
            
            if self.current_token and self.current_token.type == TT_DEDENT:
                self.advance()  # Skip DEDENT
            
            return WhenNode('document', 'scroll', actions)
        
        return None
    
    def parse_elif(self):
        """Parse elif condition"""
        self.advance()  # Skip 'elif'
        
        condition = self.parse_expression()
        
        if condition:
            if self.current_token and self.current_token.type == TT_NEWLINE:
                self.advance()
            
            if self.current_token and self.current_token.type == TT_INDENT:
                self.advance()  # Skip INDENT
                
                body = []
                while self.current_token and self.current_token.type != TT_DEDENT and self.current_token.type != TT_EOF:
                    stmt = self.parse_statement()
                    if stmt:
                        body.append(stmt)
                    else:
                        self.advance()
                
                if self.current_token and self.current_token.type == TT_DEDENT:
                    self.advance()  # Skip DEDENT
                
                return ElifNode(condition, body)
        
        return None
    
    def parse_repeat(self):
        """Parse repeat loop"""
        self.advance()  # Skip 'repeat'
        
        if self.current_token and self.current_token.type == TT_INT:
            count = self.current_token.value
            self.advance()  # Skip count
            
            if self.current_token and self.current_token.type == TT_NEWLINE:
                self.advance()
            
            if self.current_token and self.current_token.type == TT_INDENT:
                self.advance()  # Skip INDENT
                
                body = []
                while self.current_token and self.current_token.type != TT_DEDENT and self.current_token.type != TT_EOF:
                    stmt = self.parse_statement()
                    if stmt:
                        body.append(stmt)
                    else:
                        self.advance()
                
                if self.current_token and self.current_token.type == TT_DEDENT:
                    self.advance()  # Skip DEDENT
                
                return RepeatNode(count, body)
        
        return None
    
    def parse_repeat_while(self):
        """Parse repeat while loop"""
        self.advance()  # Skip 'repeatwhile'
        
        condition = self.parse_expression()
        
        if condition:
            if self.current_token and self.current_token.type == TT_NEWLINE:
                self.advance()
            
            if self.current_token and self.current_token.type == TT_INDENT:
                self.advance()  # Skip INDENT
                
                body = []
                while self.current_token and self.current_token.type != TT_DEDENT and self.current_token.type != TT_EOF:
                    stmt = self.parse_statement()
                    if stmt:
                        body.append(stmt)
                    else:
                        self.advance()
                
                if self.current_token and self.current_token.type == TT_DEDENT:
                    self.advance()  # Skip DEDENT
                
                return RepeatWhileNode(condition, body)
        
        return None
    
    def parse_for_each(self):
        """Parse for each loop"""
        self.advance()  # Skip 'for'
        
        if self.current_token and self.current_token.type == TT_IDENTIFIER:
            item = self.current_token.value
            self.advance()  # Skip item
            
            if self.current_token and self.current_token.type == TT_KEYWORD and self.current_token.value == 'in':
                self.advance()  # Skip 'in'
                
                if self.current_token and self.current_token.type == TT_IDENTIFIER:
                    list_name = self.current_token.value
                    self.advance()  # Skip list name
                    
                    if self.current_token and self.current_token.type == TT_NEWLINE:
                        self.advance()
                    
                    if self.current_token and self.current_token.type == TT_INDENT:
                        self.advance()  # Skip INDENT
                        
                        body = []
                        while self.current_token and self.current_token.type != TT_DEDENT and self.current_token.type != TT_EOF:
                            stmt = self.parse_statement()
                            if stmt:
                                body.append(stmt)
                            else:
                                self.advance()
                        
                        if self.current_token and self.current_token.type == TT_DEDENT:
                            self.advance()  # Skip DEDENT
                        
                        return ForEachNode(item, list_name, body)
        
        return None
    
    def parse_stop(self):
        """Parse stop/break"""
        self.advance()  # Skip 'stop'
        return StopNode()
    
    def parse_continue(self):
        """Parse continue"""
        self.advance()  # Skip 'continue'
        return ContinueNode()
    
    # Math Operations
    def parse_power(self):
        """Parse power operation"""
        self.advance()  # Skip 'power'
        
        if self.current_token and (self.current_token.type == TT_INT or self.current_token.type == TT_FLOAT):
            base = self.current_token.value
            self.advance()
            
            if self.current_token and (self.current_token.type == TT_INT or self.current_token.type == TT_FLOAT):
                exponent = self.current_token.value
                self.advance()
                return PowerNode(base, exponent)
        
        return None
    
    def parse_squareroot(self):
        """Parse square root"""
        self.advance()  # Skip 'squareroot'
        
        if self.current_token and (self.current_token.type == TT_INT or self.current_token.type == TT_FLOAT):
            value = self.current_token.value
            self.advance()
            return SquareRootNode(value)
        
        return None
    
    def parse_absolute(self):
        """Parse absolute value"""
        self.advance()  # Skip 'absolute'
        
        if self.current_token and (self.current_token.type == TT_INT or self.current_token.type == TT_FLOAT):
            value = self.current_token.value
            self.advance()
            return AbsoluteNode(value)
        
        return None
    
    def parse_floor(self):
        """Parse floor"""
        self.advance()  # Skip 'floor'
        
        if self.current_token and (self.current_token.type == TT_INT or self.current_token.type == TT_FLOAT):
            value = self.current_token.value
            self.advance()
            return FloorNode(value)
        
        return None
    
    def parse_ceiling(self):
        """Parse ceiling"""
        self.advance()  # Skip 'ceiling'
        
        if self.current_token and (self.current_token.type == TT_INT or self.current_token.type == TT_FLOAT):
            value = self.current_token.value
            self.advance()
            return CeilingNode(value)
        
        return None
    
    def parse_mod(self):
        """Parse modulus"""
        self.advance()  # Skip 'mod'
        
        left = self.parse_expression()
        if left:
            right = self.parse_expression()
            if right:
                return ModNode(left, right)
        
        return None
    
    # String Operations
    def parse_uppercase(self):
        """Parse uppercase"""
        self.advance()  # Skip 'uppercase'
        
        if self.current_token and self.current_token.type == TT_STRING:
            value = self.current_token.value
            self.advance()
            return UppercaseNode(value)
        
        return None
    
    def parse_lowercase(self):
        """Parse lowercase"""
        self.advance()  # Skip 'lowercase'
        
        if self.current_token and self.current_token.type == TT_STRING:
            value = self.current_token.value
            self.advance()
            return LowercaseNode(value)
        
        return None
    
    def parse_capitalize(self):
        """Parse capitalize"""
        self.advance()  # Skip 'capitalize'
        
        if self.current_token and self.current_token.type == TT_STRING:
            value = self.current_token.value
            self.advance()
            return CapitalizeNode(value)
        
        return None
    
    def parse_trim(self):
        """Parse trim"""
        self.advance()  # Skip 'trim'
        
        if self.current_token and self.current_token.type == TT_STRING:
            value = self.current_token.value
            self.advance()
            return TrimNode(value)
        
        return None
    
    def parse_replace(self):
        """Parse replace"""
        self.advance()  # Skip 'replace'
        
        if self.current_token and self.current_token.type == TT_STRING:
            string = self.current_token.value
            self.advance()
            
            if self.current_token and self.current_token.type == TT_STRING:
                old = self.current_token.value
                self.advance()
                
                if self.current_token and self.current_token.type == TT_STRING:
                    new = self.current_token.value
                    self.advance()
                    return ReplaceNode(string, old, new)
        
        return None
    
    def parse_contains(self):
        """Parse contains"""
        self.advance()  # Skip 'contains'
        
        if self.current_token and self.current_token.type == TT_STRING:
            string = self.current_token.value
            self.advance()
            
            if self.current_token and self.current_token.type == TT_STRING:
                substring = self.current_token.value
                self.advance()
                return ContainsNode(string, substring)
        
        return None
    
    def parse_startswith(self):
        """Parse startswith"""
        self.advance()  # Skip 'startswith'
        
        if self.current_token and self.current_token.type == TT_STRING:
            string = self.current_token.value
            self.advance()
            
            if self.current_token and self.current_token.type == TT_STRING:
                prefix = self.current_token.value
                self.advance()
                return StartsWithNode(string, prefix)
        
        return None
    
    def parse_endswith(self):
        """Parse endswith"""
        self.advance()  # Skip 'endswith'
        
        if self.current_token and self.current_token.type == TT_STRING:
            string = self.current_token.value
            self.advance()
            
            if self.current_token and self.current_token.type == TT_STRING:
                suffix = self.current_token.value
                self.advance()
                return EndsWithNode(string, suffix)
        
        return None
    
    def parse_lengthof(self):
        """Parse lengthof"""
        self.advance()  # Skip 'lengthof'
        
        if self.current_token and (self.current_token.type == TT_STRING or self.current_token.type == TT_IDENTIFIER):
            value = self.current_token.value
            self.advance()
            return LengthOfNode(value)
        
        return None
    
    # List Operations
    def parse_makelist(self):
        """Parse make list"""
        self.advance()  # Skip 'makelist'
        
        if self.current_token and self.current_token.type == TT_IDENTIFIER:
            name = self.current_token.value
            self.advance()
            
            if self.current_token and self.current_token.type == TT_EQUALS:
                self.advance()
                
                if self.current_token and self.current_token.type == TT_LBRACKET:
                    self.advance()
                    node = MakeListNode(name)
                    
                    while self.current_token and self.current_token.type != TT_RBRACKET:
                        if self.current_token.type == TT_INT or self.current_token.type == TT_FLOAT or self.current_token.type == TT_STRING:
                            node.items.append(self.current_token.value)
                        self.advance()
                    
                    if self.current_token and self.current_token.type == TT_RBRACKET:
                        self.advance()
                    
                    return node
        
        return None
    
    def parse_additem(self):
        """Parse add item to list"""
        self.advance()  # Skip 'additem'
        
        if self.current_token and self.current_token.type == TT_IDENTIFIER:
            list_name = self.current_token.value
            self.advance()
            
            value = self.parse_expression()
            if value:
                return AddItemNode(list_name, value)
        
        return None
    
    def parse_removeitem(self):
        """Parse remove item from list"""
        self.advance()  # Skip 'removeitem'
        
        if self.current_token and self.current_token.type == TT_IDENTIFIER:
            list_name = self.current_token.value
            self.advance()
            
            if self.current_token and (self.current_token.type == TT_INT or self.current_token.type == TT_IDENTIFIER):
                index = self.current_token.value
                self.advance()
                return RemoveItemNode(list_name, index)
        
        return None
    
    def parse_insertitem(self):
        """Parse insert item into list"""
        self.advance()  # Skip 'insertitem'
        
        if self.current_token and self.current_token.type == TT_IDENTIFIER:
            list_name = self.current_token.value
            self.advance()
            
            if self.current_token and (self.current_token.type == TT_INT or self.current_token.type == TT_IDENTIFIER):
                index = self.current_token.value
                self.advance()
                
                value = self.parse_expression()
                if value:
                    return InsertItemNode(list_name, index, value)
        
        return None
    
    def parse_sort(self):
        """Parse sort list"""
        self.advance()  # Skip 'sort'
        
        if self.current_token and self.current_token.type == TT_IDENTIFIER:
            list_name = self.current_token.value
            self.advance()
            return SortNode(list_name)
        
        return None
    
    def parse_reverse(self):
        """Parse reverse list"""
        self.advance()  # Skip 'reverse'
        
        if self.current_token and self.current_token.type == TT_IDENTIFIER:
            list_name = self.current_token.value
            self.advance()
            return ReverseNode(list_name)
        
        return None
    
    def parse_shuffle(self):
        """Parse shuffle list"""
        self.advance()  # Skip 'shuffle'
        
        if self.current_token and self.current_token.type == TT_IDENTIFIER:
            list_name = self.current_token.value
            self.advance()
            return ShuffleNode(list_name)
        
        return None
    
    def parse_listlength(self):
        """Parse list length"""
        self.advance()  # Skip 'listlength'
        
        if self.current_token and self.current_token.type == TT_IDENTIFIER:
            list_name = self.current_token.value
            self.advance()
            return ListLengthNode(list_name)
        
        return None
    
    def parse_containsitem(self):
        """Parse contains item in list"""
        self.advance()  # Skip 'containsitem'
        
        if self.current_token and self.current_token.type == TT_IDENTIFIER:
            list_name = self.current_token.value
            self.advance()
            
            value = self.parse_expression()
            if value:
                return ContainsItemNode(list_name, value)
        
        return None
    
    # Storage Operations
    def parse_sessionsave(self):
        """Parse session save"""
        self.advance()  # Skip 'sessionsave'
        
        if self.current_token and self.current_token.type == TT_IDENTIFIER:
            key = self.current_token.value
            self.advance()
            
            value = self.parse_expression()
            if value:
                return SessionSaveNode(key, value)
        
        return None
    
    def parse_cookie(self):
        """Parse cookie"""
        self.advance()  # Skip 'cookie'
        
        if self.current_token and self.current_token.type == TT_IDENTIFIER:
            key = self.current_token.value
            self.advance()
            
            value = self.parse_expression()
            if value:
                return CookieNode(key, value)
        
        return None
    
    # Database Operations
    def parse_connectdatabase(self):
        """Parse connect to database"""
        self.advance()  # Skip 'connectdatabase'
        
        if self.current_token and self.current_token.type == TT_STRING:
            connection_string = self.current_token.value
            self.advance()
            return ConnectDatabaseNode(connection_string)
        
        return None
    
    def parse_savedatabase(self):
        """Parse save to database"""
        self.advance()  # Skip 'savedatabase'
        
        if self.current_token and self.current_token.type == TT_STRING:
            collection = self.current_token.value
            self.advance()
            
            data = self.parse_expression()
            if data:
                return SaveDatabaseNode(collection, data)
        
        return None
    
    def parse_loaddatabase(self):
        """Parse load from database"""
        self.advance()  # Skip 'loaddatabase'
        
        if self.current_token and self.current_token.type == TT_STRING:
            collection = self.current_token.value
            self.advance()
            
            query = self.parse_expression()
            if query:
                return LoadDatabaseNode(collection, query)
        
        return None
    
    def parse_updatedatabase(self):
        """Parse update database"""
        self.advance()  # Skip 'updatedatabase'
        
        if self.current_token and self.current_token.type == TT_STRING:
            collection = self.current_token.value
            self.advance()
            
            query = self.parse_expression()
            if query:
                data = self.parse_expression()
                if data:
                    return UpdateDatabaseNode(collection, query, data)
        
        return None
    
    def parse_deletedatabase(self):
        """Parse delete from database"""
        self.advance()  # Skip 'deletedatabase'
        
        if self.current_token and self.current_token.type == TT_STRING:
            collection = self.current_token.value
            self.advance()
            
            query = self.parse_expression()
            if query:
                return DeleteDatabaseNode(collection, query)
        
        return None
    
    # Auth Operations
    def parse_login(self):
        """Parse login"""
        self.advance()  # Skip 'login'
        
        if self.current_token and self.current_token.type == TT_IDENTIFIER:
            username = self.current_token.value
            self.advance()
            
            if self.current_token and self.current_token.type == TT_IDENTIFIER:
                password = self.current_token.value
                self.advance()
                return LoginNode(username, password)
        
        return None
    
    def parse_logout(self):
        """Parse logout"""
        self.advance()  # Skip 'logout'
        return LogoutNode()
    
    def parse_signup(self):
        """Parse signup"""
        self.advance()  # Skip 'signup'
        
        if self.current_token and self.current_token.type == TT_IDENTIFIER:
            username = self.current_token.value
            self.advance()
            
            if self.current_token and self.current_token.type == TT_IDENTIFIER:
                password = self.current_token.value
                self.advance()
                
                if self.current_token and self.current_token.type == TT_IDENTIFIER:
                    email = self.current_token.value
                    self.advance()
                    return SignupNode(username, password, email)
        
        return None
    
    def parse_encrypt(self):
        """Parse encrypt"""
        self.advance()  # Skip 'encrypt'
        
        if self.current_token and self.current_token.type == TT_STRING:
            data = self.current_token.value
            self.advance()
            return EncryptNode(data)
        
        return None
    
    def parse_decrypt(self):
        """Parse decrypt"""
        self.advance()  # Skip 'decrypt'
        
        if self.current_token and self.current_token.type == TT_STRING:
            data = self.current_token.value
            self.advance()
            return DecryptNode(data)
        
        return None
    
    def parse_hash(self):
        """Parse hash"""
        self.advance()  # Skip 'hash'
        
        if self.current_token and self.current_token.type == TT_STRING:
            data = self.current_token.value
            self.advance()
            return HashNode(data)
        
        return None
    
    def parse_verifypassword(self):
        """Parse verify password"""
        self.advance()  # Skip 'verifypassword'
        
        if self.current_token and self.current_token.type == TT_STRING:
            password = self.current_token.value
            self.advance()
            
            if self.current_token and self.current_token.type == TT_STRING:
                hash_value = self.current_token.value
                self.advance()
                return VerifyPasswordNode(password, hash_value)
        
        return None
    
    def parse_generatetoken(self):
        """Parse generate token"""
        self.advance()  # Skip 'generatetoken'
        return GenerateTokenNode()
    
    # UI Operations
    def parse_confirm(self):
        """Parse confirm dialog"""
        self.advance()  # Skip 'confirm'
        
        if self.current_token and self.current_token.type == TT_STRING:
            message = self.current_token.value
            self.advance()
            return ConfirmNode(message)
        
        return None
    
    def parse_askuser(self):
        """Parse ask user dialog"""
        self.advance()  # Skip 'askuser'
        
        if self.current_token and self.current_token.type == TT_STRING:
            message = self.current_token.value
            self.advance()
            return AskUserNode(message)
        
        return None
    
    def parse_notification(self):
        """Parse notification"""
        self.advance()  # Skip 'notification'
        
        if self.current_token and self.current_token.type == TT_STRING:
            message = self.current_token.value
            self.advance()
            
            duration = 3000
            if self.current_token and self.current_token.type == TT_KEYWORD and self.current_token.value == 'duration':
                self.advance()
                if self.current_token and self.current_token.type == TT_INT:
                    duration = self.current_token.value
                    self.advance()
            
            return NotificationNode(message, duration)
        
        return None
    
    def parse_toast(self):
        """Parse toast message"""
        self.advance()  # Skip 'toast'
        
        if self.current_token and self.current_token.type == TT_STRING:
            message = self.current_token.value
            self.advance()
            return ToastNode(message)
        
        return None
    
    def parse_progress(self):
        """Parse progress bar"""
        self.advance()  # Skip 'progress'
        
        if self.current_token and (self.current_token.type == TT_INT or self.current_token.type == TT_FLOAT):
            value = self.current_token.value
            self.advance()
            return ProgressNode(value)
        
        return None
    
    def parse_loading(self):
        """Parse loading spinner"""
        self.advance()  # Skip 'loading'
        return LoadingNode()
    
    # State Operations
    def parse_show(self):
        """Parse show element"""
        self.advance()  # Skip 'show'
        
        if self.current_token and self.current_token.type == TT_IDENTIFIER:
            element = self.current_token.value
            self.advance()
            return ShowNode(element)
        
        return None
    
    def parse_hide(self):
        """Parse hide element"""
        self.advance()  # Skip 'hide'
        
        if self.current_token and self.current_token.type == TT_IDENTIFIER:
            element = self.current_token.value
            self.advance()
            return HideNode(element)
        
        return None
    
    def parse_enable(self):
        """Parse enable element"""
        self.advance()  # Skip 'enable'
        
        if self.current_token and self.current_token.type == TT_IDENTIFIER:
            element = self.current_token.value
            self.advance()
            return EnableNode(element)
        
        return None
    
    def parse_disable(self):
        """Parse disable element"""
        self.advance()  # Skip 'disable'
        
        if self.current_token and self.current_token.type == TT_IDENTIFIER:
            element = self.current_token.value
            self.advance()
            return DisableNode(element)
        
        return None
    
    # Animation Operations
    def parse_fadein(self):
        """Parse fade in animation"""
        self.advance()  # Skip 'fadein'
        
        element = ''
        duration = 1000
        
        if self.current_token and self.current_token.type == TT_IDENTIFIER:
            element = self.current_token.value
            self.advance()
        
        if self.current_token and self.current_token.type == TT_KEYWORD and self.current_token.value == 'duration':
            self.advance()
            if self.current_token and self.current_token.type == TT_INT:
                duration = self.current_token.value
                self.advance()
        
        return FadeInNode(element, duration)
    
    def parse_fadeout(self):
        """Parse fade out animation"""
        self.advance()  # Skip 'fadeout'
        
        element = ''
        duration = 1000
        
        if self.current_token and self.current_token.type == TT_IDENTIFIER:
            element = self.current_token.value
            self.advance()
        
        if self.current_token and self.current_token.type == TT_KEYWORD and self.current_token.value == 'duration':
            self.advance()
            if self.current_token and self.current_token.type == TT_INT:
                duration = self.current_token.value
                self.advance()
        
        return FadeOutNode(element, duration)
    
    def parse_slide(self):
        """Parse slide animation"""
        self.advance()  # Skip 'slide'
        
        element = ''
        direction = 'left'
        distance = 100
        
        if self.current_token and self.current_token.type == TT_IDENTIFIER:
            element = self.current_token.value
            self.advance()
        
        if self.current_token and self.current_token.type == TT_KEYWORD and self.current_token.value == 'direction':
            self.advance()
            if self.current_token and self.current_token.type == TT_STRING:
                direction = self.current_token.value
                self.advance()
        
        return SlideNode(element, direction, distance)
    
    def parse_grow(self):
        """Parse grow animation"""
        self.advance()  # Skip 'grow'
        
        element = ''
        scale = 1.5
        
        if self.current_token and self.current_token.type == TT_IDENTIFIER:
            element = self.current_token.value
            self.advance()
        
        if self.current_token and self.current_token.type == TT_KEYWORD and self.current_token.value == 'scale':
            self.advance()
            if self.current_token and (self.current_token.type == TT_INT or self.current_token.type == TT_FLOAT):
                scale = self.current_token.value
                self.advance()
        
        return GrowNode(element, scale)
    
    def parse_shrink(self):
        """Parse shrink animation"""
        self.advance()  # Skip 'shrink'
        
        element = ''
        scale = 0.5
        
        if self.current_token and self.current_token.type == TT_IDENTIFIER:
            element = self.current_token.value
            self.advance()
        
        if self.current_token and self.current_token.type == TT_KEYWORD and self.current_token.value == 'scale':
            self.advance()
            if self.current_token and (self.current_token.type == TT_INT or self.current_token.type == TT_FLOAT):
                scale = self.current_token.value
                self.advance()
        
        return ShrinkNode(element, scale)
    
    def parse_rotate(self):
        """Parse rotate animation"""
        self.advance()  # Skip 'rotate'
        
        element = ''
        degrees = 180
        
        if self.current_token and self.current_token.type == TT_IDENTIFIER:
            element = self.current_token.value
            self.advance()
        
        if self.current_token and self.current_token.type == TT_INT:
            degrees = self.current_token.value
            self.advance()
        
        return RotateNode(element, degrees)
    
    def parse_bounce(self):
        """Parse bounce animation"""
        self.advance()  # Skip 'bounce'
        
        element = ''
        if self.current_token and self.current_token.type == TT_IDENTIFIER:
            element = self.current_token.value
            self.advance()
        
        return BounceNode(element)
    
    def parse_spin(self):
        """Parse spin animation"""
        self.advance()  # Skip 'spin'
        
        element = ''
        if self.current_token and self.current_token.type == TT_IDENTIFIER:
            element = self.current_token.value
            self.advance()
        
        return SpinNode(element)
    
    def parse_shake(self):
        """Parse shake animation"""
        self.advance()  # Skip 'shake'
        
        element = ''
        if self.current_token and self.current_token.type == TT_IDENTIFIER:
            element = self.current_token.value
            self.advance()
        
        return ShakeNode(element)
    
    def parse_moveto(self):
        """Parse move to position"""
        self.advance()  # Skip 'moveto'
        
        element = ''
        x = 0
        y = 0
        
        if self.current_token and self.current_token.type == TT_IDENTIFIER:
            element = self.current_token.value
            self.advance()
        
        if self.current_token and self.current_token.type == TT_IDENTIFIER and self.current_token.value == 'x':
            self.advance()
            if self.current_token and self.current_token.type == TT_INT:
                x = self.current_token.value
                self.advance()
        
        if self.current_token and self.current_token.type == TT_IDENTIFIER and self.current_token.value == 'y':
            self.advance()
            if self.current_token and self.current_token.type == TT_INT:
                y = self.current_token.value
                self.advance()
        
        return MoveToNode(element, x, y)
    
    def parse_moveby(self):
        """Parse move by relative amount"""
        self.advance()  # Skip 'moveby'
        
        element = ''
        dx = 0
        dy = 0
        
        if self.current_token and self.current_token.type == TT_IDENTIFIER:
            element = self.current_token.value
            self.advance()
        
        if self.current_token and self.current_token.type == TT_IDENTIFIER and self.current_token.value == 'dx':
            self.advance()
            if self.current_token and self.current_token.type == TT_INT:
                dx = self.current_token.value
                self.advance()
        
        if self.current_token and self.current_token.type == TT_IDENTIFIER and self.current_token.value == 'dy':
            self.advance()
            if self.current_token and self.current_token.type == TT_INT:
                dy = self.current_token.value
                self.advance()
        
        return MoveByNode(element, dx, dy)
    
    def parse_fliphorizontal(self):
        """Parse flip horizontal"""
        self.advance()  # Skip 'fliphorizontal'
        
        element = ''
        if self.current_token and self.current_token.type == TT_IDENTIFIER:
            element = self.current_token.value
            self.advance()
        
        return FlipHorizontalNode(element)
    
    def parse_flipvertical(self):
        """Parse flip vertical"""
        self.advance()  # Skip 'flipvertical'
        
        element = ''
        if self.current_token and self.current_token.type == TT_IDENTIFIER:
            element = self.current_token.value
            self.advance()
        
        return FlipVerticalNode(element)
    
    def parse_animate(self):
        """Parse custom animation"""
        self.advance()  # Skip 'animate'
        
        element = ''
        animation = ''
        duration = 500
        
        if self.current_token and self.current_token.type == TT_IDENTIFIER:
            element = self.current_token.value
            self.advance()
        
        if self.current_token and self.current_token.type == TT_STRING:
            animation = self.current_token.value
            self.advance()
        
        if self.current_token and self.current_token.type == TT_KEYWORD and self.current_token.value == 'duration':
            self.advance()
            if self.current_token and self.current_token.type == TT_INT:
                duration = self.current_token.value
                self.advance()
        
        return AnimateNode(element, animation, duration)
    
    # Web Navigation
    def parse_openwebsite(self):
        """Parse open website"""
        self.advance()  # Skip 'openwebsite'
        
        if self.current_token and self.current_token.type == TT_STRING:
            url = self.current_token.value
            self.advance()
            return OpenWebsiteNode(url)
        
        return None
    
    def parse_sharepage(self):
        """Parse share page"""
        self.advance()  # Skip 'sharepage'
        return SharePageNode()
    
    def parse_copylink(self):
        """Parse copy link"""
        self.advance()  # Skip 'copylink'
        return CopyLinkNode()
    
    def parse_printpage(self):
        """Parse print page"""
        self.advance()  # Skip 'printpage'
        return PrintPageNode()
    
    # File Operations
    def parse_savefile(self):
        """Parse save file"""
        self.advance()  # Skip 'savefile'
        
        content = self.parse_expression()
        if content:
            if self.current_token and self.current_token.type == TT_STRING:
                filename = self.current_token.value
                self.advance()
                return SaveFileNode(content, filename)
        
        return None
    
    def parse_openfile(self):
        """Parse open file"""
        self.advance()  # Skip 'openfile'
        
        if self.current_token and self.current_token.type == TT_STRING:
            filename = self.current_token.value
            self.advance()
            return OpenFileNode(filename)
        
        return None
    
    def parse_deletefile(self):
        """Parse delete file"""
        self.advance()  # Skip 'deletefile'
        
        if self.current_token and self.current_token.type == TT_STRING:
            filename = self.current_token.value
            self.advance()
            return DeleteFileNode(filename)
        
        return None
    
    def parse_renamefile(self):
        """Parse rename file"""
        self.advance()  # Skip 'renamefile'
        
        if self.current_token and self.current_token.type == TT_STRING:
            old_name = self.current_token.value
            self.advance()
            
            if self.current_token and self.current_token.type == TT_STRING:
                new_name = self.current_token.value
                self.advance()
                return RenameFileNode(old_name, new_name)
        
        return None
    
    # Media Operations
    def parse_stop_media(self):
        """Parse stop media"""
        self.advance()  # Skip 'stop'
        
        if self.current_token and self.current_token.type == TT_IDENTIFIER:
            element = self.current_token.value
            self.advance()
            return StopMediaNode(element)
        
        return None
    
    def parse_camera(self):
        """Parse camera access"""
        self.advance()  # Skip 'camera'
        return CameraNode()
    
    def parse_takephoto(self):
        """Parse take photo"""
        self.advance()  # Skip 'takephoto'
        return TakePhotoNode()
    
    def parse_recordvideo(self):
        """Parse record video"""
        self.advance()  # Skip 'recordvideo'
        return RecordVideoNode()
    
    def parse_microphone(self):
        """Parse microphone access"""
        self.advance()  # Skip 'microphone'
        return MicrophoneNode()
    
    def parse_recordaudio(self):
        """Parse record audio"""
        self.advance()  # Skip 'recordaudio'
        return RecordAudioNode()
    
    # Action/Function Operations
    def parse_action(self):
        """Parse action/function definition"""
        self.advance()  # Skip 'action'
        
        if self.current_token and self.current_token.type == TT_IDENTIFIER:
            name = self.current_token.value
            self.advance()
            
            params = []
            # Check for parameters
            if self.current_token and self.current_token.type == TT_IDENTIFIER:
                while self.current_token and self.current_token.type == TT_IDENTIFIER:
                    params.append(self.current_token.value)
                    self.advance()
            
            if self.current_token and self.current_token.type == TT_NEWLINE:
                self.advance()
            
            if self.current_token and self.current_token.type == TT_INDENT:
                self.advance()  # Skip INDENT
                
                body = []
                while self.current_token and self.current_token.type != TT_DEDENT and self.current_token.type != TT_EOF:
                    stmt = self.parse_statement()
                    if stmt:
                        body.append(stmt)
                    else:
                        self.advance()
                
                if self.current_token and self.current_token.type == TT_DEDENT:
                    self.advance()  # Skip DEDENT
                
                return ActionNode(name, params, body)
        
        return None
    
    def parse_run(self):
        """Parse run/call action"""
        self.advance()  # Skip 'run'
        
        if self.current_token and self.current_token.type == TT_IDENTIFIER:
            name = self.current_token.value
            self.advance()
            
            args = []
            while self.current_token and (self.current_token.type == TT_INT or self.current_token.type == TT_FLOAT or 
                                         self.current_token.type == TT_STRING or self.current_token.type == TT_IDENTIFIER):
                args.append(self.current_token.value)
                self.advance()
            
            return RunNode(name, args)
        
        return None
    
    def parse_return(self):
        """Parse return statement"""
        self.advance()  # Skip 'return'
        
        value = self.parse_expression()
        return ReturnNode(value)
    
    def parse_component(self):
        """Parse component definition"""
        self.advance()  # Skip 'component'
        
        if self.current_token and self.current_token.type == TT_IDENTIFIER:
            name = self.current_token.value
            self.advance()
            
            if self.current_token and self.current_token.type == TT_NEWLINE:
                self.advance()
            
            if self.current_token and self.current_token.type == TT_INDENT:
                self.advance()  # Skip INDENT
                
                body = []
                while self.current_token and self.current_token.type != TT_DEDENT and self.current_token.type != TT_EOF:
                    stmt = self.parse_statement()
                    if stmt:
                        body.append(stmt)
                    else:
                        self.advance()
                
                if self.current_token and self.current_token.type == TT_DEDENT:
                    self.advance()  # Skip DEDENT
                
                return ComponentNode(name, body)
        
        return None
    
    def parse_use(self):
        """Parse use component"""
        self.advance()  # Skip 'use'
        
        if self.current_token and self.current_token.type == TT_IDENTIFIER:
            name = self.current_token.value
            self.advance()
            return UseNode(name)
        
        return None
    
    def parse_state(self):
        """Parse state declaration"""
        self.advance()  # Skip 'state'
        
        if self.current_token and self.current_token.type == TT_IDENTIFIER:
            name = self.current_token.value
            self.advance()
            
            if self.current_token and self.current_token.type == TT_EQUALS:
                self.advance()
                
                value = self.parse_expression()
                if value:
                    return StateNode(name, value)
        
        return None
    
    # HTTP Request Operations
    def parse_puttoserver(self):
        """Parse PUT request"""
        self.advance()  # Skip 'puttoserver'
        
        if self.current_token and self.current_token.type == TT_STRING:
            url = self.current_token.value
            self.advance()
            
            data = self.parse_expression()
            if data:
                return PutToServerNode(url, data)
        
        return None
    
    def parse_deletefromserver(self):
        """Parse DELETE request"""
        self.advance()  # Skip 'deletefromserver'
        
        if self.current_token and self.current_token.type == TT_STRING:
            url = self.current_token.value
            self.advance()
            return DeleteFromServerNode(url)
        
        return None
    
    def parse_fetch(self):
        """Parse fetch request"""
        self.advance()  # Skip 'fetch'
        
        if self.current_token and self.current_token.type == TT_STRING:
            url = self.current_token.value
            self.advance()
            return FetchNode(url)
        
        return None
    
# parser.py - Add server parsing methods

    def parse_route(self):
        """Parse route definition"""
        self.advance()  # Skip 'route'
        
        if self.current_token and self.current_token.type == TT_STRING:
            path = self.current_token.value
            self.advance()
            
            method = 'GET'
            if self.current_token and self.current_token.type == TT_KEYWORD and self.current_token.value in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
                method = self.current_token.value
                self.advance()
            
            if self.current_token and self.current_token.type == TT_COLON:
                self.advance()
                
                if self.current_token and self.current_token.type == TT_NEWLINE:
                    self.advance()
                
                if self.current_token and self.current_token.type == TT_INDENT:
                    self.advance()
                    
                    body = []
                    while self.current_token and self.current_token.type != TT_DEDENT and self.current_token.type != TT_EOF:
                        stmt = self.parse_statement()
                        if stmt:
                            body.append(stmt)
                        else:
                            self.advance()
                    
                    if self.current_token and self.current_token.type == TT_DEDENT:
                        self.advance()
                    
                    return RouteNode(path, method, body)
        
        return None

# parser.py - Add database parsing methods

    def parse_connectdatabase(self):
        """Parse connect to database"""
        self.advance()  # Skip 'connectdatabase'
        
        if self.current_token and self.current_token.type == TT_STRING:
            connection_string = self.current_token.value
            self.advance()
            return ConnectDatabaseNode(connection_string)
        
        return None
    
    def parse_savedatabase(self):
        """Parse save to database"""
        self.advance()  # Skip 'savedatabase'
        
        if self.current_token and self.current_token.type == TT_STRING:
            collection = self.current_token.value
            self.advance()
            
            data = self.parse_expression()
            if data:
                return SaveDatabaseNode(collection, data)
        
        return None
    
    def parse_loaddatabase(self):
        """Parse load from database"""
        self.advance()  # Skip 'loaddatabase'
        
        if self.current_token and self.current_token.type == TT_STRING:
            collection = self.current_token.value
            self.advance()
            
            query = self.parse_expression()
            if query:
                return LoadDatabaseNode(collection, query)
        
        return None
    
    def parse_updatedatabase(self):
        """Parse update database"""
        self.advance()  # Skip 'updatedatabase'
        
        if self.current_token and self.current_token.type == TT_STRING:
            collection = self.current_token.value
            self.advance()
            
            query = self.parse_expression()
            if query:
                data = self.parse_expression()
                if data:
                    return UpdateDatabaseNode(collection, query, data)
        
        return None
    
    def parse_deletedatabase(self):
        """Parse delete from database"""
        self.advance()  # Skip 'deletedatabase'
        
        if self.current_token and self.current_token.type == TT_STRING:
            collection = self.current_token.value
            self.advance()
            
            query = self.parse_expression()
            if query:
                return DeleteDatabaseNode(collection, query)
        
        return None