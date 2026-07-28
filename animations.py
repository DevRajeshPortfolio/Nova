# animations.py
# Nova Programming Language - Advanced Animation Framework

import json
import time
from datetime import datetime

class Animation:
    """Animation definition"""
    
    def __init__(self, name, keyframes, options=None):
        self.name = name
        self.keyframes = keyframes
        self.options = options or {
            'duration': 1000,
            'timing': 'ease',
            'iteration': 1,
            'direction': 'normal',
            'fill_mode': 'forwards'
        }
    
    def to_css(self):
        """Convert animation to CSS"""
        css = f"@keyframes {self.name} {{\n"
        for percentage, styles in self.keyframes.items():
            css += f"    {percentage}% {{\n"
            for prop, value in styles.items():
                css += f"        {prop}: {value};\n"
            css += "    }\n"
        css += "}\n\n"
        
        # Utility class
        css += f".anim-{self.name} {{\n"
        css += f"    animation-name: {self.name};\n"
        css += f"    animation-duration: {self.options['duration']}ms;\n"
        css += f"    animation-timing-function: {self.options['timing']};\n"
        css += f"    animation-iteration-count: {self.options['iteration']};\n"
        css += f"    animation-direction: {self.options['direction']};\n"
        css += f"    animation-fill-mode: {self.options['fill_mode']};\n"
        css += "}\n\n"
        
        return css


class AnimationSequence:
    """Sequence of animations"""
    
    def __init__(self, name, animations, delays=None):
        self.name = name
        self.animations = animations
        self.delays = delays or [0] * len(animations)
    
    def to_css(self):
        """Convert sequence to CSS"""
        css = f"/* Animation Sequence: {self.name} */\n"
        for i, (anim, delay) in enumerate(zip(self.animations, self.delays)):
            css += f".anim-seq-{self.name}-{i} {{\n"
            css += f"    animation: {anim} {delay}ms forwards;\n"
            css += "}\n\n"
        return css


class AnimationGroup:
    """Group of parallel animations"""
    
    def __init__(self, name, animations):
        self.name = name
        self.animations = animations
    
    def to_css(self):
        """Convert group to CSS"""
        css = f"/* Animation Group: {self.name} */\n"
        for anim in self.animations:
            css += f".anim-group-{self.name} .{anim} {{\n"
            css += f"    animation-play-state: running;\n"
            css += "}\n\n"
        return css


class AnimationEngine:
    """Animation engine"""
    
    def __init__(self):
        self.animations = {}
        self.sequences = {}
        self.groups = {}
        self._animating_elements = {}
    
    def define_animation(self, name, keyframes, options=None):
        """Define an animation"""
        anim = Animation(name, keyframes, options)
        self.animations[name] = anim
        return anim
    
    def define_sequence(self, name, animations, delays=None):
        """Define an animation sequence"""
        seq = AnimationSequence(name, animations, delays)
        self.sequences[name] = seq
        return seq
    
    def define_group(self, name, animations):
        """Define an animation group"""
        group = AnimationGroup(name, animations)
        self.groups[name] = group
        return group
    
    def animate_element(self, element_id, animation_name, options=None):
        """Animate an element"""
        if options is None:
            options = {}
        
        # Get animation
        anim = self.animations.get(animation_name)
        if not anim:
            return {'success': False, 'error': 'Animation not found'}
        
        # Apply animation
        js = f"""
        const element = document.getElementById("{element_id}");
        if (!element) return;
        
        // Apply CSS animation
        element.style.animation = "{animation_name} {anim.options['duration']}ms {anim.options['timing']} {anim.options['iteration']} {anim.options['direction']}";
        element.style.animationFillMode = "{anim.options['fill_mode']}";
        
        // Handle completion
        if ({options.get('on_complete', 'null')}) {{
            element.addEventListener('animationend', function handler() {{
                {options.get('on_complete', '')}
                element.removeEventListener('animationend', handler);
            }});
        }}
        """
        return {'success': True, 'js': js}
    
    def animate_sequence(self, element_id, sequence_name):
        """Animate element with a sequence"""
        seq = self.sequences.get(sequence_name)
        if not seq:
            return {'success': False, 'error': 'Sequence not found'}
        
        js = f"""
        const element = document.getElementById("{element_id}");
        if (!element) return;
        
        // Apply sequence
        const animations = {json.dumps(seq.animations)};
        const delays = {json.dumps(seq.delays)};
        let totalDelay = 0;
        
        animations.forEach((anim, index) => {{
            const delay = delays[index] || 0;
            setTimeout(() => {{
                element.style.animation = anim + " " + (delay || 300) + "ms forwards";
            }}, totalDelay);
            totalDelay += delay || 300;
        }});
        """
        return {'success': True, 'js': js}
    
    def generate_all_css(self):
        """Generate all animation CSS"""
        css = "/* Nova Animations */\n\n"
        
        for anim in self.animations.values():
            css += anim.to_css()
        
        for seq in self.sequences.values():
            css += seq.to_css()
        
        for group in self.groups.values():
            css += group.to_css()
        
        # Add common animations
        css += self._add_common_animations()
        
        return css
    
    def _add_common_animations(self):
        """Add common predefined animations"""
        return """
        /* Fade In */
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        /* Fade Out */
        @keyframes fadeOut {
            from { opacity: 1; }
            to { opacity: 0; }
        }
        
        /* Slide Up */
        @keyframes slideUp {
            from { transform: translateY(50px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        /* Slide Down */
        @keyframes slideDown {
            from { transform: translateY(-50px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        /* Slide Left */
        @keyframes slideLeft {
            from { transform: translateX(50px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        /* Slide Right */
        @keyframes slideRight {
            from { transform: translateX(-50px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        /* Bounce */
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-20px); }
        }
        
        /* Pulse */
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        /* Shake */
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-10px); }
            75% { transform: translateX(10px); }
        }
        
        /* Spin */
        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        
        /* Zoom In */
        @keyframes zoomIn {
            from { transform: scale(0.5); opacity: 0; }
            to { transform: scale(1); opacity: 1; }
        }
        
        /* Zoom Out */
        @keyframes zoomOut {
            from { transform: scale(1); opacity: 1; }
            to { transform: scale(0.5); opacity: 0; }
        }
        
        /* Utility classes */
        .fade-in { animation: fadeIn 0.5s ease forwards; }
        .fade-out { animation: fadeOut 0.5s ease forwards; }
        .slide-up { animation: slideUp 0.5s ease forwards; }
        .slide-down { animation: slideDown 0.5s ease forwards; }
        .slide-left { animation: slideLeft 0.5s ease forwards; }
        .slide-right { animation: slideRight 0.5s ease forwards; }
        .bounce { animation: bounce 0.5s ease; }
        .pulse { animation: pulse 0.5s ease; }
        .shake { animation: shake 0.5s ease; }
        .spin { animation: spin 1s linear infinite; }
        .zoom-in { animation: zoomIn 0.5s ease forwards; }
        .zoom-out { animation: zoomOut 0.5s ease forwards; }
        """
    
    def generate_animation_js(self):
        """Generate animation JavaScript helper"""
        return """
        // Nova Animation Helpers
        class NovaAnimation {
            static animate(element, animation, duration = 500, callback = null) {
                const el = typeof element === 'string' ? document.getElementById(element) : element;
                if (!el) return;
                
                // Apply animation
                el.style.animation = `${animation} ${duration}ms ease forwards`;
                
                if (callback) {
                    el.addEventListener('animationend', function handler() {
                        callback();
                        el.removeEventListener('animationend', handler);
                    });
                }
            }
            
            static fadeIn(element, duration = 500, callback = null) {
                this.animate(element, 'fadeIn', duration, callback);
            }
            
            static fadeOut(element, duration = 500, callback = null) {
                this.animate(element, 'fadeOut', duration, callback);
            }
            
            static slideUp(element, duration = 500, callback = null) {
                this.animate(element, 'slideUp', duration, callback);
            }
            
            static slideDown(element, duration = 500, callback = null) {
                this.animate(element, 'slideDown', duration, callback);
            }
            
            static bounce(element, duration = 500, callback = null) {
                this.animate(element, 'bounce', duration, callback);
            }
            
            static pulse(element, duration = 500, callback = null) {
                this.animate(element, 'pulse', duration, callback);
            }
            
            static shake(element, duration = 500, callback = null) {
                this.animate(element, 'shake', duration, callback);
            }
            
            static zoomIn(element, duration = 500, callback = null) {
                this.animate(element, 'zoomIn', duration, callback);
            }
            
            static zoomOut(element, duration = 500, callback = null) {
                this.animate(element, 'zoomOut', duration, callback);
            }
            
            static sequence(element, animations, durations = null) {
                const el = typeof element === 'string' ? document.getElementById(element) : element;
                if (!el) return;
                
                let totalDelay = 0;
                animations.forEach((anim, index) => {
                    const duration = (durations && durations[index]) || 500;
                    setTimeout(() => {
                        this.animate(el, anim, duration);
                    }, totalDelay);
                    totalDelay += duration;
                });
            }
            
            static parallel(element, animations, duration = 500) {
                const el = typeof element === 'string' ? document.getElementById(element) : element;
                if (!el) return;
                
                animations.forEach(anim => {
                    this.animate(el, anim, duration);
                });
            }
            
            static stop(element) {
                const el = typeof element === 'string' ? document.getElementById(element) : element;
                if (el) {
                    el.style.animation = 'none';
                }
            }
        }
        
        // Make global
        window.NovaAnimation = NovaAnimation;
        """