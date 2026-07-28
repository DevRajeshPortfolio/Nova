# html_generator.py
# Nova Programming Language - HTML Generator

class HTMLGenerator:
    def __init__(self):
        self.html = ''
        self.indent_level = 0
        self.input_counter = 0
    
    def generate(self, ast):
        """Generate HTML from AST"""
        self.html = '<!DOCTYPE html>\n'
        self.html += '<html>\n'
        self.html += '<head>\n'
        self.html += '    <meta charset="UTF-8">\n'
        self.html += '    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        self.html += '    <title>Nova Page</title>\n'
        self.html += '    <link rel="stylesheet" href="style.css">\n'
        
        # CSS Animations
        self.html += '    <style>\n'
        self.html += '        /* Animations */\n'
        self.html += '        @keyframes bounce {\n'
        self.html += '            0%, 100% { transform: translateY(0); }\n'
        self.html += '            50% { transform: translateY(-20px); }\n'
        self.html += '        }\n'
        self.html += '        @keyframes spin {\n'
        self.html += '            from { transform: rotate(0deg); }\n'
        self.html += '            to { transform: rotate(360deg); }\n'
        self.html += '        }\n'
        self.html += '        @keyframes shake {\n'
        self.html += '            0%, 100% { transform: translateX(0); }\n'
        self.html += '            25% { transform: translateX(-10px); }\n'
        self.html += '            75% { transform: translateX(10px); }\n'
        self.html += '        }\n'
        self.html += '        @keyframes pulse {\n'
        self.html += '            0%, 100% { transform: scale(1); }\n'
        self.html += '            50% { transform: scale(1.05); }\n'
        self.html += '        }\n'
        self.html += '        @keyframes fadeIn {\n'
        self.html += '            from { opacity: 0; }\n'
        self.html += '            to { opacity: 1; }\n'
        self.html += '        }\n'
        self.html += '        @keyframes slideIn {\n'
        self.html += '            from { transform: translateX(-100%); }\n'
        self.html += '            to { transform: translateX(0); }\n'
        self.html += '        }\n'
        self.html += '        @keyframes fadeOut {\n'
        self.html += '            from { opacity: 1; }\n'
        self.html += '            to { opacity: 0; }\n'
        self.html += '        }\n'
        self.html += '        @keyframes slideOut {\n'
        self.html += '            from { transform: translateX(0); }\n'
        self.html += '            to { transform: translateX(100%); }\n'
        self.html += '        }\n'
        self.html += '        @keyframes rotateIn {\n'
        self.html += '            from { transform: rotate(-180deg); opacity: 0; }\n'
        self.html += '            to { transform: rotate(0deg); opacity: 1; }\n'
        self.html += '        }\n'
        self.html += '        @keyframes zoomIn {\n'
        self.html += '            from { transform: scale(0.5); opacity: 0; }\n'
        self.html += '            to { transform: scale(1); opacity: 1; }\n'
        self.html += '        }\n'
        self.html += '        @keyframes zoomOut {\n'
        self.html += '            from { transform: scale(1); opacity: 1; }\n'
        self.html += '            to { transform: scale(0.5); opacity: 0; }\n'
        self.html += '        }\n'
        self.html += '        @keyframes flip {\n'
        self.html += '            from { transform: rotateY(0deg); }\n'
        self.html += '            to { transform: rotateY(180deg); }\n'
        self.html += '        }\n'
        self.html += '        @keyframes flipIn {\n'
        self.html += '            from { transform: rotateY(90deg); opacity: 0; }\n'
        self.html += '            to { transform: rotateY(0deg); opacity: 1; }\n'
        self.html += '        }\n'
        self.html += '        @keyframes slideUp {\n'
        self.html += '            from { transform: translateY(50px); opacity: 0; }\n'
        self.html += '            to { transform: translateY(0); opacity: 1; }\n'
        self.html += '        }\n'
        self.html += '        @keyframes slideDown {\n'
        self.html += '            from { transform: translateY(-50px); opacity: 0; }\n'
        self.html += '            to { transform: translateY(0); opacity: 1; }\n'
        self.html += '        }\n'
        self.html += '        @keyframes slideLeft {\n'
        self.html += '            from { transform: translateX(50px); opacity: 0; }\n'
        self.html += '            to { transform: translateX(0); opacity: 1; }\n'
        self.html += '        }\n'
        self.html += '        @keyframes slideRight {\n'
        self.html += '            from { transform: translateX(-50px); opacity: 0; }\n'
        self.html += '            to { transform: translateX(0); opacity: 1; }\n'
        self.html += '        }\n'
        
        # Animation utility classes
        self.html += '        .anim-bounce { animation: bounce 0.5s ease; }\n'
        self.html += '        .anim-spin { animation: spin 1s linear infinite; }\n'
        self.html += '        .anim-shake { animation: shake 0.5s ease; }\n'
        self.html += '        .anim-pulse { animation: pulse 0.5s ease; }\n'
        self.html += '        .anim-fadeIn { animation: fadeIn 0.5s ease; }\n'
        self.html += '        .anim-fadeOut { animation: fadeOut 0.5s ease; }\n'
        self.html += '        .anim-slideIn { animation: slideIn 0.5s ease; }\n'
        self.html += '        .anim-slideOut { animation: slideOut 0.5s ease; }\n'
        self.html += '        .anim-rotateIn { animation: rotateIn 0.5s ease; }\n'
        self.html += '        .anim-zoomIn { animation: zoomIn 0.5s ease; }\n'
        self.html += '        .anim-zoomOut { animation: zoomOut 0.5s ease; }\n'
        self.html += '        .anim-flip { animation: flip 0.5s ease; }\n'
        self.html += '        .anim-flipIn { animation: flipIn 0.5s ease; }\n'
        self.html += '        .anim-slideUp { animation: slideUp 0.5s ease; }\n'
        self.html += '        .anim-slideDown { animation: slideDown 0.5s ease; }\n'
        self.html += '        .anim-slideLeft { animation: slideLeft 0.5s ease; }\n'
        self.html += '        .anim-slideRight { animation: slideRight 0.5s ease; }\n'
        self.html += '    </style>\n'
        
        self.html += '</head>\n'
        self.html += '<body>\n'
        
        self.html += '    <div class="nova-container">\n'
        self.indent_level = 1
        
        for node in ast:
            self.generate_node(node)
        
        self.indent_level = 0
        self.html += '    </div>\n'
        self.html += '    <script src="script.js"></script>\n'
        self.html += '</body>\n'
        self.html += '</html>'
        return self.html
    
    def generate_node(self, node):
        if node.node_type == 'Page':
            self.generate_page(node)
        elif node.node_type == 'Button':
            self.generate_button(node)
        elif node.node_type == 'NumberInput':
            self.generate_number_input(node)
        elif node.node_type == 'Text':
            self.generate_text(node)
        elif node.node_type == 'Heading':
            self.generate_heading(node)
        elif node.node_type == 'Subtitle':
            self.generate_subtitle(node)
        elif node.node_type == 'Small':
            self.generate_small(node)
        elif node.node_type == 'Quote':
            self.generate_quote(node)
        elif node.node_type == 'Code':
            self.generate_code(node)
        elif node.node_type == 'Link':
            self.generate_link(node)
        elif node.node_type == 'Label':
            self.generate_label(node)
        elif node.node_type == 'Input':
            self.generate_input(node)
        elif node.node_type == 'Password':
            self.generate_password(node)
        elif node.node_type == 'Email':
            self.generate_email(node)
        elif node.node_type == 'Search':
            self.generate_search(node)
        elif node.node_type == 'Textarea':
            self.generate_textarea(node)
        elif node.node_type == 'Checkbox':
            self.generate_checkbox(node)
        elif node.node_type == 'Radio':
            self.generate_radio(node)
        elif node.node_type == 'Dropdown':
            self.generate_dropdown(node)
        elif node.node_type == 'Date':
            self.generate_date(node)
        elif node.node_type == 'Time':
            self.generate_time(node)
        elif node.node_type == 'Colour':
            self.generate_colour(node)
        elif node.node_type == 'Slider':
            self.generate_slider(node)
        elif node.node_type == 'Upload':
            self.generate_upload(node)
        elif node.node_type == 'Title':
            self.generate_title(node)
        elif node.node_type == 'Background':
            self.generate_background(node)
        # NEW NODE TYPES
        elif node.node_type == 'Image':
            self.generate_image(node)
        elif node.node_type == 'Video':
            self.generate_video(node)
        elif node.node_type == 'Audio':
            self.generate_audio(node)
        elif node.node_type == 'Gallery':
            self.generate_gallery(node)
        elif node.node_type == 'Slideshow':
            self.generate_slideshow(node)
        elif node.node_type == 'Container':
            self.generate_container(node)
        elif node.node_type == 'Card':
            self.generate_card(node)
        elif node.node_type == 'Section':
            self.generate_section(node)
        elif node.node_type == 'Navbar':
            self.generate_navbar(node)
        elif node.node_type == 'Footer':
            self.generate_footer(node)
        elif node.node_type == 'Sidebar':
            self.generate_sidebar(node)
        elif node.node_type == 'Row':
            self.generate_row(node)
        elif node.node_type == 'Column':
            self.generate_column(node)
        elif node.node_type == 'Grid':
            self.generate_grid(node)
        elif node.node_type == 'Tabs':
            self.generate_tabs(node)
        elif node.node_type == 'Panel':
            self.generate_panel(node)
        elif node.node_type == 'Group':
            self.generate_group(node)
        # POSITION NODE
        elif node.node_type == 'Position':
            self.generate_position(node)
        else:
            # Default handling
            self.html += self.indent() + f'<!-- {node.node_type} -->\n'
    
    def generate_style_attributes(self, node):
        """Generate inline style from node.style dictionary"""
        if not node.style:
            return ''
        style_str = ' style="'
        for key, value in node.style.items():
            style_str += f'{key}: {value}; '
        style_str += '"'
        return style_str
    
    def generate_page(self, page_node):
        # Handle title if present
        for child in page_node.children:
            if child.node_type == 'Title':
                self.html = self.html.replace('<title>Nova Page</title>', f'<title>{child.text}</title>')
            elif child.node_type == 'Background':
                self.generate_background(child)
        
        # Generate all other children
        for child in page_node.children:
            if child.node_type not in ['Title', 'Background']:
                self.generate_node(child)
    
    def generate_button(self, button_node):
        style = self.generate_style_attributes(button_node)
        self.html += self.indent() + f'<button id="{button_node.name}" class="nova-button"{style}>{button_node.text}</button>\n'
    
    def generate_number_input(self, input_node):
        style = self.generate_style_attributes(input_node)
        self.html += self.indent() + f'<div class="nova-input-group"{style}>\n'
        self.indent_level += 1
        self.html += self.indent() + f'<label for="{input_node.name}" class="nova-label">{input_node.name}</label>\n'
        self.html += self.indent() + f'<input type="number" id="{input_node.name}" class="nova-input" value="{input_node.value}">\n'
        self.indent_level -= 1
        self.html += self.indent() + f'</div>\n'
    
    def generate_text(self, text_node):
        style = self.generate_style_attributes(text_node)
        self.html += self.indent() + f'<p class="nova-text"{style}>{text_node.content}</p>\n'
    
    def generate_heading(self, heading_node):
        style = self.generate_style_attributes(heading_node)
        self.html += self.indent() + f'<h1 class="nova-heading"{style}>{heading_node.content}</h1>\n'
    
    def generate_subtitle(self, subtitle_node):
        style = self.generate_style_attributes(subtitle_node)
        self.html += self.indent() + f'<h2 class="nova-subtitle"{style}>{subtitle_node.content}</h2>\n'
    
    def generate_small(self, small_node):
        style = self.generate_style_attributes(small_node)
        self.html += self.indent() + f'<small class="nova-small"{style}>{small_node.content}</small>\n'
    
    def generate_quote(self, quote_node):
        style = self.generate_style_attributes(quote_node)
        self.html += self.indent() + f'<blockquote class="nova-quote"{style}>{quote_node.content}</blockquote>\n'
    
    def generate_code(self, code_node):
        style = self.generate_style_attributes(code_node)
        self.html += self.indent() + f'<code class="nova-code"{style}>{code_node.content}</code>\n'
    
    def generate_link(self, link_node):
        style = self.generate_style_attributes(link_node)
        self.html += self.indent() + f'<a href="{link_node.url}" class="nova-link"{style}>{link_node.text}</a>\n'
    
    def generate_label(self, label_node):
        style = self.generate_style_attributes(label_node)
        self.html += self.indent() + f'<label class="nova-label"{style}>{label_node.text}</label>\n'
    
    def generate_input(self, input_node):
        style = self.generate_style_attributes(input_node)
        self.html += self.indent() + f'<div class="nova-input-group"{style}>\n'
        self.indent_level += 1
        self.html += self.indent() + f'<label for="{input_node.name}" class="nova-label">{input_node.name}</label>\n'
        self.html += self.indent() + f'<input type="text" id="{input_node.name}" class="nova-input" placeholder="{input_node.placeholder}">\n'
        self.indent_level -= 1
        self.html += self.indent() + f'</div>\n'
    
    def generate_password(self, password_node):
        style = self.generate_style_attributes(password_node)
        self.html += self.indent() + f'<div class="nova-input-group"{style}>\n'
        self.indent_level += 1
        self.html += self.indent() + f'<label for="{password_node.name}" class="nova-label">{password_node.name}</label>\n'
        self.html += self.indent() + f'<input type="password" id="{password_node.name}" class="nova-input">\n'
        self.indent_level -= 1
        self.html += self.indent() + f'</div>\n'
    
    def generate_email(self, email_node):
        style = self.generate_style_attributes(email_node)
        self.html += self.indent() + f'<div class="nova-input-group"{style}>\n'
        self.indent_level += 1
        self.html += self.indent() + f'<label for="{email_node.name}" class="nova-label">{email_node.name}</label>\n'
        self.html += self.indent() + f'<input type="email" id="{email_node.name}" class="nova-input" value="{email_node.value}">\n'
        self.indent_level -= 1
        self.html += self.indent() + f'</div>\n'
    
    def generate_search(self, search_node):
        style = self.generate_style_attributes(search_node)
        self.html += self.indent() + f'<div class="nova-input-group"{style}>\n'
        self.indent_level += 1
        self.html += self.indent() + f'<label for="{search_node.name}" class="nova-label">{search_node.name}</label>\n'
        self.html += self.indent() + f'<input type="search" id="{search_node.name}" class="nova-input">\n'
        self.indent_level -= 1
        self.html += self.indent() + f'</div>\n'
    
    def generate_textarea(self, textarea_node):
        style = self.generate_style_attributes(textarea_node)
        self.html += self.indent() + f'<div class="nova-input-group"{style}>\n'
        self.indent_level += 1
        self.html += self.indent() + f'<label for="{textarea_node.name}" class="nova-label">{textarea_node.name}</label>\n'
        self.html += self.indent() + f'<textarea id="{textarea_node.name}" class="nova-textarea" rows="{textarea_node.rows}" cols="{textarea_node.cols}">{textarea_node.value}</textarea>\n'
        self.indent_level -= 1
        self.html += self.indent() + f'</div>\n'
    
    def generate_checkbox(self, checkbox_node):
        checked = ' checked' if checkbox_node.checked else ''
        style = self.generate_style_attributes(checkbox_node)
        self.html += self.indent() + f'<div class="nova-checkbox-group"{style}>\n'
        self.indent_level += 1
        self.html += self.indent() + f'<input type="checkbox" id="{checkbox_node.name}" class="nova-checkbox"{checked}>\n'
        self.html += self.indent() + f'<label for="{checkbox_node.name}" class="nova-label">{checkbox_node.label or checkbox_node.name}</label>\n'
        self.indent_level -= 1
        self.html += self.indent() + f'</div>\n'
    
    def generate_radio(self, radio_node):
        checked = ' checked' if radio_node.checked else ''
        style = self.generate_style_attributes(radio_node)
        self.html += self.indent() + f'<div class="nova-radio-group"{style}>\n'
        self.indent_level += 1
        self.html += self.indent() + f'<input type="radio" id="{radio_node.name}_{radio_node.value}" name="{radio_node.name}" class="nova-radio" value="{radio_node.value}"{checked}>\n'
        self.html += self.indent() + f'<label for="{radio_node.name}_{radio_node.value}" class="nova-label">{radio_node.label}</label>\n'
        self.indent_level -= 1
        self.html += self.indent() + f'</div>\n'
    
    def generate_dropdown(self, dropdown_node):
        style = self.generate_style_attributes(dropdown_node)
        self.html += self.indent() + f'<div class="nova-input-group"{style}>\n'
        self.indent_level += 1
        self.html += self.indent() + f'<label for="{dropdown_node.name}" class="nova-label">{dropdown_node.name}</label>\n'
        self.html += self.indent() + f'<select id="{dropdown_node.name}" class="nova-dropdown">\n'
        self.indent_level += 1
        for option in dropdown_node.options:
            selected = ' selected' if option == dropdown_node.selected else ''
            self.html += self.indent() + f'<option value="{option}"{selected}>{option}</option>\n'
        self.indent_level -= 1
        self.html += self.indent() + f'</select>\n'
        self.indent_level -= 1
        self.html += self.indent() + f'</div>\n'
    
    def generate_date(self, date_node):
        style = self.generate_style_attributes(date_node)
        self.html += self.indent() + f'<div class="nova-input-group"{style}>\n'
        self.indent_level += 1
        self.html += self.indent() + f'<label for="{date_node.name}" class="nova-label">{date_node.name}</label>\n'
        self.html += self.indent() + f'<input type="date" id="{date_node.name}" class="nova-input">\n'
        self.indent_level -= 1
        self.html += self.indent() + f'</div>\n'
    
    def generate_time(self, time_node):
        style = self.generate_style_attributes(time_node)
        self.html += self.indent() + f'<div class="nova-input-group"{style}>\n'
        self.indent_level += 1
        self.html += self.indent() + f'<label for="{time_node.name}" class="nova-label">{time_node.name}</label>\n'
        self.html += self.indent() + f'<input type="time" id="{time_node.name}" class="nova-input">\n'
        self.indent_level -= 1
        self.html += self.indent() + f'</div>\n'
    
    def generate_colour(self, colour_node):
        style = self.generate_style_attributes(colour_node)
        self.html += self.indent() + f'<div class="nova-input-group"{style}>\n'
        self.indent_level += 1
        self.html += self.indent() + f'<label for="{colour_node.name}" class="nova-label">{colour_node.name}</label>\n'
        self.html += self.indent() + f'<input type="color" id="{colour_node.name}" class="nova-colour" value="{colour_node.value}">\n'
        self.indent_level -= 1
        self.html += self.indent() + f'</div>\n'
    
    def generate_slider(self, slider_node):
        style = self.generate_style_attributes(slider_node)
        self.html += self.indent() + f'<div class="nova-input-group"{style}>\n'
        self.indent_level += 1
        self.html += self.indent() + f'<label for="{slider_node.name}" class="nova-label">{slider_node.name}: <span id="{slider_node.name}_value">{slider_node.value}</span></label>\n'
        self.html += self.indent() + f'<input type="range" id="{slider_node.name}" class="nova-slider" min="{slider_node.min}" max="{slider_node.max}" value="{slider_node.value}">\n'
        self.indent_level -= 1
        self.html += self.indent() + f'</div>\n'
        # Add JS to update slider value display
        self.html += self.indent() + f'<script>\n'
        self.html += self.indent() + f'    document.getElementById("{slider_node.name}").addEventListener("input", function() {{\n'
        self.html += self.indent() + f'        document.getElementById("{slider_node.name}_value").textContent = this.value;\n'
        self.html += self.indent() + f'    }});\n'
        self.html += self.indent() + f'</script>\n'
    
    def generate_upload(self, upload_node):
        style = self.generate_style_attributes(upload_node)
        self.html += self.indent() + f'<div class="nova-input-group"{style}>\n'
        self.indent_level += 1
        self.html += self.indent() + f'<label for="{upload_node.name}" class="nova-label">{upload_node.name}</label>\n'
        self.html += self.indent() + f'<input type="file" id="{upload_node.name}" class="nova-upload" accept="{upload_node.accept}">\n'
        self.indent_level -= 1
        self.html += self.indent() + f'</div>\n'
    
    def generate_title(self, title_node):
        # Handled in page generation
        pass
    
    def generate_background(self, background_node):
        self.html += self.indent() + f'<style>\n'
        self.html += self.indent() + f'    body {{ background-color: {background_node.color}; }}\n'
        self.html += self.indent() + f'</style>\n'
    
    # NEW GENERATOR METHODS
    
    def generate_image(self, image_node):
        style = self.generate_style_attributes(image_node)
        self.html += self.indent() + f'<img src="{image_node.src}" alt="{image_node.alt}" class="nova-image"{style}>\n'
    
    def generate_video(self, video_node):
        style = self.generate_style_attributes(video_node)
        self.html += self.indent() + f'<video src="{video_node.src}" controls class="nova-video"{style}></video>\n'
    
    def generate_audio(self, audio_node):
        style = self.generate_style_attributes(audio_node)
        self.html += self.indent() + f'<audio src="{audio_node.src}" controls class="nova-audio"{style}></audio>\n'
    
    def generate_gallery(self, gallery_node):
        style = self.generate_style_attributes(gallery_node)
        self.html += self.indent() + f'<div class="nova-gallery"{style}>\n'
        self.indent_level += 1
        for img in gallery_node.images:
            self.html += self.indent() + f'<img src="{img}" alt="Gallery image" class="nova-gallery-image">\n'
        self.indent_level -= 1
        self.html += self.indent() + f'</div>\n'
    
    def generate_slideshow(self, slideshow_node):
        style = self.generate_style_attributes(slideshow_node)
        self.html += self.indent() + f'<div class="nova-slideshow"{style}>\n'
        self.indent_level += 1
        # Add images
        for i, img in enumerate(slideshow_node.images):
            display = 'block' if i == 0 else 'none'
            self.html += self.indent() + f'<img src="{img}" alt="Slide {i+1}" class="nova-slide" style="display:{display}">\n'
        self.indent_level -= 1
        self.html += self.indent() + f'</div>\n'
        # Add slideshow controls
        if len(slideshow_node.images) > 1:
            self.html += self.indent() + f'<div class="nova-slideshow-controls">\n'
            self.indent_level += 1
            self.html += self.indent() + f'<button class="nova-slideshow-prev">❮</button>\n'
            self.html += self.indent() + f'<button class="nova-slideshow-next">❯</button>\n'
            self.indent_level -= 1
            self.html += self.indent() + f'</div>\n'
    
    def generate_container(self, container_node):
        style = self.generate_style_attributes(container_node)
        self.html += self.indent() + f'<div class="nova-container"{style}>\n'
        self.indent_level += 1
        for child in container_node.children:
            self.generate_node(child)
        self.indent_level -= 1
        self.html += self.indent() + f'</div>\n'
    
    def generate_card(self, card_node):
        style = self.generate_style_attributes(card_node)
        self.html += self.indent() + f'<div class="nova-card"{style}>\n'
        self.indent_level += 1
        if card_node.title:
            self.html += self.indent() + f'<h3 class="nova-card-title">{card_node.title}</h3>\n'
        for child in card_node.children:
            self.generate_node(child)
        self.indent_level -= 1
        self.html += self.indent() + f'</div>\n'
    
    def generate_section(self, section_node):
        style = self.generate_style_attributes(section_node)
        self.html += self.indent() + f'<section class="nova-section"{style}>\n'
        self.indent_level += 1
        if section_node.title:
            self.html += self.indent() + f'<h2 class="nova-section-title">{section_node.title}</h2>\n'
        for child in section_node.children:
            self.generate_node(child)
        self.indent_level -= 1
        self.html += self.indent() + f'</section>\n'
    
    def generate_navbar(self, navbar_node):
        style = self.generate_style_attributes(navbar_node)
        self.html += self.indent() + f'<nav class="nova-navbar"{style}>\n'
        self.indent_level += 1
        self.html += self.indent() + f'<ul class="nova-navbar-list">\n'
        self.indent_level += 1
        for item in navbar_node.items:
            self.html += self.indent() + f'<li><a href="{item.url}" class="nova-nav-link">{item.text}</a></li>\n'
        self.indent_level -= 1
        self.html += self.indent() + f'</ul>\n'
        self.indent_level -= 1
        self.html += self.indent() + f'</nav>\n'
    
    def generate_footer(self, footer_node):
        style = self.generate_style_attributes(footer_node)
        self.html += self.indent() + f'<footer class="nova-footer"{style}>\n'
        self.indent_level += 1
        for child in footer_node.children:
            self.generate_node(child)
        self.indent_level -= 1
        self.html += self.indent() + f'</footer>\n'
    
    def generate_sidebar(self, sidebar_node):
        style = self.generate_style_attributes(sidebar_node)
        self.html += self.indent() + f'<aside class="nova-sidebar"{style}>\n'
        self.indent_level += 1
        for child in sidebar_node.children:
            self.generate_node(child)
        self.indent_level -= 1
        self.html += self.indent() + f'</aside>\n'
    
    def generate_row(self, row_node):
        style = self.generate_style_attributes(row_node)
        self.html += self.indent() + f'<div class="nova-row"{style}>\n'
        self.indent_level += 1
        for child in row_node.children:
            self.generate_node(child)
        self.indent_level -= 1
        self.html += self.indent() + f'</div>\n'
    
    def generate_column(self, column_node):
        style = self.generate_style_attributes(column_node)
        self.html += self.indent() + f'<div class="nova-column"{style}>\n'
        self.indent_level += 1
        for child in column_node.children:
            self.generate_node(child)
        self.indent_level -= 1
        self.html += self.indent() + f'</div>\n'
    
    def generate_grid(self, grid_node):
        style = self.generate_style_attributes(grid_node)
        self.html += self.indent() + f'<div class="nova-grid"{style} style="grid-template-columns: repeat({grid_node.columns}, 1fr);">\n'
        self.indent_level += 1
        for child in grid_node.children:
            self.generate_node(child)
        self.indent_level -= 1
        self.html += self.indent() + f'</div>\n'
    
    def generate_tabs(self, tabs_node):
        style = self.generate_style_attributes(tabs_node)
        self.html += self.indent() + f'<div class="nova-tabs"{style}>\n'
        self.indent_level += 1
        # Tab headers
        self.html += self.indent() + f'<div class="nova-tab-headers">\n'
        self.indent_level += 1
        for i, tab in enumerate(tabs_node.tabs):
            active = ' active' if i == 0 else ''
            self.html += self.indent() + f'<button class="nova-tab-btn{active}" data-tab="{i}">{tab.title}</button>\n'
        self.indent_level -= 1
        self.html += self.indent() + f'</div>\n'
        # Tab content
        for i, tab in enumerate(tabs_node.tabs):
            display = 'block' if i == 0 else 'none'
            self.html += self.indent() + f'<div class="nova-tab-content" data-tab="{i}" style="display:{display}">\n'
            self.indent_level += 1
            for child in tab.children:
                self.generate_node(child)
            self.indent_level -= 1
            self.html += self.indent() + f'</div>\n'
        self.indent_level -= 1
        self.html += self.indent() + f'</div>\n'
    
    def generate_panel(self, panel_node):
        style = self.generate_style_attributes(panel_node)
        self.html += self.indent() + f'<div class="nova-panel"{style}>\n'
        self.indent_level += 1
        if panel_node.title:
            self.html += self.indent() + f'<div class="nova-panel-header">{panel_node.title}</div>\n'
        self.html += self.indent() + f'<div class="nova-panel-body">\n'
        self.indent_level += 1
        for child in panel_node.children:
            self.generate_node(child)
        self.indent_level -= 1
        self.html += self.indent() + f'</div>\n'
        self.indent_level -= 1
        self.html += self.indent() + f'</div>\n'
    
    def generate_group(self, group_node):
        style = self.generate_style_attributes(group_node)
        self.html += self.indent() + f'<div class="nova-group"{style}>\n'
        self.indent_level += 1
        for child in group_node.children:
            self.generate_node(child)
        self.indent_level -= 1
        self.html += self.indent() + f'</div>\n'
    
    def generate_position(self, position_node):
        """Generate position node with exact x,y coordinates"""
        style = f' style="position: absolute; left: {position_node.x}px; top: {position_node.y}px;"'
        if position_node.element:
            # Position an existing element
            self.html += self.indent() + f'<div id="position_{position_node.element}" class="nova-absolute"{style}>\n'
            # The element will be placed inside this container
            # We need to actually move the element - handled in JS
        else:
            # Position container
            self.html += self.indent() + f'<div class="nova-absolute"{style}>\n'
            self.indent_level += 1
            for child in position_node.children:
                self.generate_node(child)
            self.indent_level -= 1
            self.html += self.indent() + f'</div>\n'
    
    def indent(self):
        return '    ' * self.indent_level

# html_generator.py - Add VDOM support

    def generate_with_vdom(self, ast):
        """Generate HTML with VDOM support"""
        self.html = '<!DOCTYPE html>\n'
        self.html += '<html>\n'
        self.html += '<head>\n'
        self.html += '    <meta charset="UTF-8">\n'
        self.html += '    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        self.html += '    <title>Nova VDOM App</title>\n'
        self.html += '    <link rel="stylesheet" href="style.css">\n'
        self.html += '</head>\n'
        self.html += '<body>\n'
        self.html += '    <div id="app"></div>\n'
        self.html += '    <script src="vdom-runtime.js"></script>\n'
        self.html += '    <script>\n'
        self.html += '        // VDOM Runtime\n'
        self.html += self._generate_vdom_runtime(ast)
        self.html += '    </script>\n'
        self.html += '</body>\n'
        self.html += '</html>'
        return self.html
    
    def _generate_vdom_runtime(self, ast):
        """Generate VDOM runtime JavaScript"""
        js = '''
        const { h, text, VirtualDOM, ReactiveComponent } = NovaVDOM;
        
        // Create reactive state
        const state = new VirtualDOM().createReactiveState({});
        
        // Define components
        class App extends ReactiveComponent {
            render() {
                return h('div', { className: 'nova-container' },
'''
        # Build component tree from AST
        for node in ast:
            js += self._node_to_vdom(node)
        
        js += '''
                );
            }
        }
        
        // Mount app
        const app = new App();
        app.mount(document.getElementById('app'));
        '''
        return js
    
    def _node_to_vdom(self, node):
        """Convert AST node to VDOM expression"""
        if node.node_type == 'Text':
            return f'                    h("p", {{ className: "nova-text" }}, "{node.content}"),\n'
        elif node.node_type == 'Heading':
            return f'                    h("h1", {{ className: "nova-heading" }}, "{node.content}"),\n'
        elif node.node_type == 'Button':
            return f'''                    h("button", {{ 
                        className: "nova-button", 
                        id: "{node.name}",
                        onClick: () => alert("Button clicked!")
                    }}, "{node.text}"),\n'''
        elif node.node_type == 'Input':
            return f'''                    h("div", {{ className: "nova-input-group" }},
                        h("label", {{ className: "nova-label", htmlFor: "{node.name}" }}, "{node.name}"),
                        h("input", {{ 
                            type: "text", 
                            id: "{node.name}", 
                            className: "nova-input",
                            placeholder: "{node.placeholder or ''}"
                        }})
                    ),\n'''
        return ''

# html_generator.py - Add component support

    def generate_with_components(self, ast):
        """Generate HTML with component support"""
        from components import ComponentRegistry, render_components, node_to_component
        
        registry = ComponentRegistry()
        
        # First pass: register all components
        for node in ast:
            if node.node_type == 'Component':
                from components import component_from_ast
                comp = component_from_ast([node], registry)
                if comp:
                    registry.register(node.name, comp)
        
        # Second pass: render components
        html = '<!DOCTYPE html>\n'
        html += '<html>\n<head>\n'
        html += '    <meta charset="UTF-8">\n'
        html += '    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        html += '    <title>Nova Components</title>\n'
        html += '    <link rel="stylesheet" href="style.css">\n'
        html += '</head>\n<body>\n'
        html += '    <div id="app"></div>\n'
        html += '    <script>\n'
        html += '        // Component Runtime\n'
        html += self._generate_component_runtime(ast, registry)
        html += '    </script>\n'
        html += '</body>\n</html>'
        return html
    
    def _generate_component_runtime(self, ast, registry):
        """Generate component runtime JavaScript"""
        js = '''
        // VDOM Runtime
        const { h, text, VirtualDOM, ReactiveComponent } = NovaVDOM;
        
        // Component Registry
        const components = {};
        
        // State management
        const appState = new VirtualDOM().createReactiveState({});
        
        // Define components
'''
        # Generate component definitions
        for name, comp in registry.components.items():
            js += f'''
        class Component_{name} extends ReactiveComponent {{
            render() {{
                return h('div', {{ className: 'nova-component-{name}' }},
                    // Component content from AST
'''
            # Find component node in AST
            for node in ast:
                if hasattr(node, 'name') and node.name == name:
                    for child in node.body:
                        js += self._node_to_component_js(child)
            js += '''
                );
            }
        }}
        components['{name}'] = Component_{name};
'''
        
        js += '''
        // App component
        class App extends ReactiveComponent {
            render() {
                return h('div', { className: 'nova-container' },
'''
        # Render top-level components
        for node in ast:
            if node.node_type == 'Use':
                js += f'                    h(components["{node.name}"], {{}}),\n'
            elif node.node_type != 'Component':
                js += self._node_to_component_js(node)
        
        js += '''
                );
            }
        }
        
        // Mount app
        const app = new App();
        app.mount(document.getElementById('app'));
        '''
        return js
    
    def _node_to_component_js(self, node):
        """Convert AST node to component JavaScript"""
        if node.node_type == 'Text':
            return f'                    h("p", {{ className: "nova-text" }}, "{node.content}"),\n'
        elif node.node_type == 'Heading':
            return f'                    h("h1", {{ className: "nova-heading" }}, "{node.content}"),\n'
        elif node.node_type == 'Button':
            return f'''                    h("button", {{ 
                        className: "nova-button", 
                        id: "{node.name}",
                        onClick: () => alert("Button clicked!")
                    }}, "{node.text}"),\n'''
        elif node.node_type == 'Input':
            return f'''                    h("div", {{ className: "nova-input-group" }},
                        h("label", {{ className: "nova-label", htmlFor: "{node.name}" }}, "{node.name}"),
                        h("input", {{ 
                            type: "text", 
                            id: "{node.name}", 
                            className: "nova-input",
                            placeholder: "{getattr(node, 'placeholder', '')}"
                        }})
                    ),\n'''
        return ''