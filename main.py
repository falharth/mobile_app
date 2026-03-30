from kivy.app import App  # Import the base App class from Kivy framework
from kivy.uix.image import Image  # Import the Image widget to display pictures
from kivy.uix.floatlayout import FloatLayout  # Import layout that positions widgets by relative coordinates
from kivy.uix.label import Label  # Import Label widget to display text
from kivy.uix.button import Button  # Import Button widget for clickable buttons
from kivy.uix.popup import Popup  # Import Popup widget for dialog boxes
from kivy.uix.boxlayout import BoxLayout  # Import BoxLayout for arranging widgets vertically
from kivy.uix.scrollview import ScrollView  # Import ScrollView for scrollable content
from kivy.uix.behaviors import ButtonBehavior  # Import ButtonBehavior to make any widget clickable
from kivy.core.window import Window  # Import the Window module to control window settings
from kivy.graphics import Rectangle, Color, Ellipse, Line, RoundedRectangle  # Import drawing tools
from kivy.clock import Clock  # Import Clock for scheduling animations
from kivy.utils import platform  # Import platform to detect iOS vs desktop
import random  # Import random for star positions
import os  # Import os for file path handling
from datetime import datetime  # Import datetime for live clock

# Get the directory where main.py lives (needed for iOS file paths)
APP_DIR = os.path.dirname(os.path.abspath(__file__))  # Base path for loading images


def open_url(url):  # Open a URL — works on both iOS and desktop
    if platform == 'ios':  # On iPhone, use native iOS API
        from pyobjus import autoclass  # Import Objective-C bridge (available on iOS)
        NSUrl = autoclass('NSURL')  # Get NSURL class
        UIApp = autoclass('UIApplication')  # Get UIApplication class
        shared = UIApp.sharedApplication()  # Get the running app instance
        ns_url = NSUrl.URLWithString_(url)  # Convert string to NSURL
        shared.openURL_(ns_url)  # Open URL in Safari
    else:  # On desktop (Windows/Mac/Linux)
        import webbrowser  # Use standard webbrowser module
        webbrowser.open(url)  # Open URL in default browser


class ClickableImage(ButtonBehavior, Image):  # Combine ButtonBehavior + Image to make a clickable image
    def on_press(self):  # Called when finger touches the image
        self.color = (1, 0.3, 0.3, 1)  # Red shine on touch press

    def on_release(self):  # Called when finger lifts off the image
        self.color = (1, 1, 1, 1)  # Normal color when touch ends


class GreenScreenApp(App):  # Create our app class that inherits from Kivy's App
    def build(self):  # This method is called when the app starts
        Window.clearcolor = (0.02, 0.0, 0.1, 1)  # Deep dark space background color

        self.layout = FloatLayout()  # Create a layout to hold everything

        # Create a list to store star data for animation
        self.stars = []
        for _ in range(150):  # Create 150 animated stars
            star = {
                'x': random.uniform(0, Window.width),  # Random x position
                'y': random.uniform(0, Window.height),  # Random y position
                'speed': random.uniform(0.3, 2.0),  # Random movement speed
                'size': random.uniform(1, 3.5),  # Random star size
                'brightness': random.uniform(0.7, 1.0),  # Random brightness
                'alpha': random.uniform(0.4, 1.0),  # Random transparency
            }
            self.stars.append(star)

        # Create fire particles around the subtitle text
        self.fire_particles = []
        for _ in range(60):  # Create 60 fire particles
            particle = {
                'x': random.uniform(Window.width * 0.2, Window.width * 0.8),  # Spread across subtitle width
                'y': Window.height * 0.08 + random.uniform(-15, 15),  # Around subtitle y position
                'vx': random.uniform(-0.5, 0.5),  # Horizontal drift speed
                'vy': random.uniform(0.5, 2.5),  # Upward speed (fire rises)
                'size': random.uniform(2, 6),  # Random particle size
                'life': random.uniform(0, 1.0),  # Current life (0 = new, 1 = fading)
                'max_life': random.uniform(0.5, 1.0),  # How long before respawn
            }
            self.fire_particles.append(particle)

        # Draw initial background
        self._draw_background()

        # Schedule animation update 60 times per second
        Clock.schedule_interval(self._animate_stars, 1 / 60)  # Update stars every frame

        # Welcome text at the top
        welcome = Label(text='Welcome to Faisal\'s App',  # Welcome sentence
                        font_size='28sp',  # Font size
                        color=(0.7, 0.5, 1, 1),  # Light purple text color (galaxy theme)
                        bold=True,  # Bold text
                        size_hint=(1, 0.1),  # Take full width, 10% height
                        pos_hint={'center_x': 0.5, 'top': 0.97})  # Position at top center
        self.layout.add_widget(welcome)  # Add welcome text to layout

        # Subtitle text
        subtitle = Label(text='Explore the Universe of Trading',  # Subtitle text
                         font_size='16sp',  # Smaller font
                         color=(0.5, 0.8, 1, 0.8),  # Light blue text
                         size_hint=(1, 0.05),  # Full width, 5% height
                         pos_hint={'center_x': 0.5, 'top': 0.08})  # Below the welcome text
        self.layout.add_widget(subtitle)  # Add subtitle to layout

        # Profile image in center (use full path for iOS compatibility)
        img = Image(source=os.path.join(APP_DIR, 'Faisal.png'),  # Load the profile image
                    size_hint=(0.55, 0.55),  # Image takes 45% of screen
                    pos_hint={'center_x': 0.5, 'center_y': 0.5})  # Center on screen
        self.layout.add_widget(img)  # Add the image to the layout

        # Live clock display at top-right corner (lowered for iPhone notch safe area)
        self.clock_label = Label(text='',  # Will be updated every second
                                 font_size='14sp',  # Small font size
                                 color=(0.8, 0.8, 1, 0.7),  # Soft light color
                                 size_hint=(0.3, 0.05),  # Small size
                                 pos_hint={'right': 0.98, 'top': 0.93})  # Below iPhone notch area
        self.layout.add_widget(self.clock_label)  # Add clock to layout
        Clock.schedule_interval(self._update_clock, 1)  # Update clock every second
        self._update_clock(0)  # Set initial time

        # --- "Trade History" button ---
        history_btn = Button(text='Trade History',  # Button label
                             font_size='16sp',  # Font size
                             size_hint=(0.4, 0.07),  # 40% width, 7% height (touch-friendly)
                             pos_hint={'x': 0.05, 'y': 0.2},  # Left side
                             background_color=(0.4, 0.1, 0.6, 0.85),  # Purple galaxy color
                             color=(1, 1, 1, 1),  # White text
                             bold=True)  # Bold text
        history_btn.bind(on_press=self.show_history_popup)  # Open popup on tap
        self.layout.add_widget(history_btn)  # Add button to layout

        # --- "Market News" button ---
        news_btn = Button(text='Learn How?',  # Button label
                          font_size='16sp',  # Font size
                          size_hint=(0.4, 0.07),  # 40% width, 7% height (touch-friendly)
                          pos_hint={'right': 0.95, 'y': 0.2},  # Right side
                          background_color=(0.1, 0.3, 0.6, 0.85),  # Blue galaxy color
                          color=(1, 1, 1, 1),  # White text
                          bold=True)  # Bold text
        news_btn.bind(on_press=self.open_market_news)  # Open news website on tap
        self.layout.add_widget(news_btn)  # Add button to layout

        # --- "About" button --- (lowered for iPhone notch safe area)
        about_btn = Button(text='About',  # Button label
                           font_size='14sp',  # Readable font
                           size_hint=(0.2, 0.06),  # Larger tap target for fingers
                           pos_hint={'x': 0.02, 'top': 0.93},  # Below iPhone notch area
                           background_color=(0.3, 0.3, 0.5, 0.7),  # Subtle purple
                           color=(1, 1, 1, 0.9))  # White text
        about_btn.bind(on_press=self.show_about_popup)  # Open about popup on tap
        self.layout.add_widget(about_btn)  # Add button to layout

        # Tap adx.png image to open ADX website (touch-friendly size, full path for iOS)
        img2 = ClickableImage(source=os.path.join(APP_DIR, 'adx.png'),  # Load adx.png with full path
                              size_hint=(0.35, 0.12),  # Larger tap target for iPhone fingers
                              pos_hint={'center_x': 0.5, 'y': 0.1})  # Position at bottom center
        img2.bind(on_press=self.open_website)  # When image is pressed, call open_website method
        self.layout.add_widget(img2)  # Add the clickable image to the layout

        return self.layout  # Return the galaxy-themed layout

    def _draw_background(self):  # Draw the galaxy background with current star positions
        self.layout.canvas.before.clear()  # Clear previous frame
        with self.layout.canvas.before:
            Color(0.02, 0.0, 0.1, 1)  # Dark space background
            Rectangle(pos=(0, 0), size=Window.size)  # Fill background

            # Draw nebula clouds (stationary)
            Color(0.3, 0.0, 0.5, 0.15)  # Purple nebula glow
            Ellipse(pos=(Window.width * 0.15, Window.height * 0.3),
                    size=(Window.width * 0.7, Window.height * 0.5))
            Color(0.0, 0.2, 0.6, 0.1)  # Blue nebula glow
            Ellipse(pos=(Window.width * 0.25, Window.height * 0.2),
                    size=(Window.width * 0.5, Window.height * 0.4))

            # Draw each star at its current position
            for star in self.stars:
                Color(star['brightness'], star['brightness'] * 0.9, 0.2, star['alpha'])  # Yellow-gold color
                Ellipse(pos=(star['x'], star['y']),  # Star position
                        size=(star['size'], star['size']))  # Star size

            # Draw fire particles around subtitle text
            for p in self.fire_particles:
                fade = max(0, 1.0 - p['life'])  # Fade out as life increases
                r = 1.0  # Red stays full
                g = 0.4 * fade + 0.1  # Green fades from orange to dark red
                b = 0.0  # No blue (pure fire color)
                Color(r, g, b, fade * 0.8)  # Fire color with fading alpha
                Ellipse(pos=(p['x'], p['y']),  # Particle position
                        size=(p['size'] * fade, p['size'] * fade))  # Shrink as it fades

    def _animate_stars(self, dt):  # Called every frame to move stars and fire
        for star in self.stars:
            star['x'] -= star['speed']  # Move star to the left (galaxy drift effect)
            star['y'] -= star['speed'] * 0.3  # Slight downward drift for diagonal movement
            # If star goes off screen, wrap it back to the right side
            if star['x'] < -5:
                star['x'] = Window.width + random.uniform(0, 20)  # Reset to right edge
                star['y'] = random.uniform(0, Window.height)  # Random new y position
            if star['y'] < -5:
                star['y'] = Window.height + random.uniform(0, 20)  # Reset to top edge
                star['x'] = random.uniform(0, Window.width)  # Random new x position

        # Animate fire particles around subtitle
        for p in self.fire_particles:
            p['x'] += p['vx']  # Move horizontally (slight drift)
            p['y'] += p['vy']  # Move upward (fire rises)
            p['life'] += dt * 1.5  # Age the particle
            # Respawn particle when it fades out
            if p['life'] >= p['max_life']:
                p['x'] = random.uniform(Window.width * 0.2, Window.width * 0.8)  # Reset x near subtitle
                p['y'] = Window.height * 0.08 + random.uniform(-10, 10)  # Reset y near subtitle
                p['vx'] = random.uniform(-0.5, 0.5)  # New random horizontal drift
                p['vy'] = random.uniform(0.5, 2.5)  # New random upward speed
                p['size'] = random.uniform(2, 6)  # New random size
                p['life'] = 0  # Reset life
                p['max_life'] = random.uniform(0.5, 1.0)  # New random lifespan

        self._draw_background()  # Redraw with updated positions

    def _update_clock(self, dt):  # Update the clock label with current time
        now = datetime.now()  # Get current date and time
        self.clock_label.text = now.strftime('%H:%M:%S  |  %d %b %Y')  # Format as HH:MM:SS | DD Mon YYYY

    def open_website(self, instance):  # Method called when the ADX image is tapped
        open_url('https://www.adx.ae/ar-AE/all-equities')  # Open the ADX website (iOS + desktop)

    def open_market_news(self, instance):  # Method called when Market News button is tapped
        open_url('https://youtu.be/TYjFce-yN5o?si=4oprhcS5UmLz6zjp')  # Open video (iOS + desktop)

    def show_history_popup(self, instance):  # Show popup with trade market history
        # Create scrollable content
        scroll = ScrollView(size_hint=(1, 1))  # Scrollable area
        history_text = (
            '[b]The History of the Trade Market[/b]\n\n'
            '[color=ffcc66]Ancient Trading (3000 BC)[/color]\n'
            'Trade began in ancient Mesopotamia and Egypt, where merchants exchanged '
            'goods like grain, spices, and textiles along trade routes.\n\n'
            '[color=ffcc66]The Silk Road (200 BC - 1400 AD)[/color]\n'
            'The famous Silk Road connected East Asia to Europe, enabling the exchange '
            'of silk, gold, spices, and ideas across civilizations.\n\n'
            '[color=ffcc66]Stock Exchanges Born (1600s)[/color]\n'
            'The Amsterdam Stock Exchange was founded in 1602 by the Dutch East India '
            'Company, becoming the world\'s first official stock exchange.\n\n'
            '[color=ffcc66]Wall Street Era (1792)[/color]\n'
            'The New York Stock Exchange was established under a buttonwood tree on '
            'Wall Street, starting with 24 stockbrokers.\n\n'
            '[color=ffcc66]Modern Electronic Trading (1971)[/color]\n'
            'NASDAQ became the world\'s first electronic stock market, revolutionizing '
            'how trades are executed globally.\n\n'
            '[color=ffcc66]Abu Dhabi Securities Exchange (2000)[/color]\n'
            'ADX was established on November 15, 2000, becoming one of the leading '
            'exchanges in the Middle East, listing major UAE companies.\n\n'
            '[color=ffcc66]Today\'s Market[/color]\n'
            'Global markets now trade trillions of dollars daily using AI, algorithms, '
            'and blockchain technology, connecting millions of investors worldwide.'
        )
        content_label = Label(text=history_text,  # The history text content
                              markup=True,  # Enable bold/color markup
                              font_size='14sp',  # Readable font size
                              color=(0.9, 0.9, 1, 1),  # Light text
                              size_hint_y=None,  # Allow height to grow
                              text_size=(Window.width * 0.7, None),  # Wrap text within width
                              halign='left',  # Left-align text
                              valign='top')  # Top-align text
        content_label.bind(texture_size=content_label.setter('size'))  # Auto-resize to fit text
        scroll.add_widget(content_label)  # Add label to scroll view

        # Create and show the popup
        popup = Popup(title='History of the Trade Market',  # Popup title
                      content=scroll,  # Scrollable content
                      size_hint=(0.85, 0.75),  # 85% width, 75% height
                      background_color=(0.05, 0.02, 0.15, 0.95),  # Dark galaxy background
                      title_color=(0.9, 0.7, 1, 1),  # Purple title color
                      title_size='18sp',  # Title font size
                      separator_color=(0.5, 0.2, 0.8, 1))  # Purple separator line
        popup.open()  # Show the popup

    def show_about_popup(self, instance):  # Show popup with app info
        about_text = (
            '[b]Faisal\'s Trading App[/b]\n\n'
            'Version 1.0\n\n'
            'A galaxy-themed trading companion app.\n\n'
            'Features:\n'
            '- Live ADX market access\n'
            '- Trade market history\n'
            '- Market news\n\n'
            'Built with Python & Kivy'
        )
        content_label = Label(text=about_text,  # About text
                              markup=True,  # Enable bold markup
                              font_size='15sp',  # Font size
                              color=(0.9, 0.9, 1, 1),  # Light text
                              text_size=(Window.width * 0.6, None),  # Wrap text
                              halign='center',  # Center-align
                              valign='middle')  # Middle-align
        content_label.bind(texture_size=content_label.setter('size'))  # Auto-resize
        popup = Popup(title='About',  # Popup title
                      content=content_label,  # Content
                      size_hint=(0.7, 0.5),  # 70% width, 50% height
                      background_color=(0.05, 0.02, 0.15, 0.95),  # Dark background
                      title_color=(0.9, 0.7, 1, 1),  # Purple title
                      title_size='18sp',  # Title size
                      separator_color=(0.5, 0.2, 0.8, 1))  # Purple separator
        popup.open()  # Show the popup





if __name__ == '__main__':  # Only run the app if this script is executed directly
    GreenScreenApp().run()  # Create an instance of the app and start it
