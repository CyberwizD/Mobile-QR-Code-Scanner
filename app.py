from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.progressbar import ProgressBar
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.metrics import dp
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.list import OneLineListItem, TwoLineListItem, ThreeLineListItem, OneLineIconListItem
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.theming import ThemeManager
import requests
import json
import threading
import time
from datetime import datetime
import cv2
import numpy as np
from pyzbar import pyzbar
from PIL import Image as PILImage
import io
import base64

# Configuration
API_BASE_URL = "http://localhost:8000"

class SecureLinkApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.accent_palette = "Purple"
        self.user_token = None
        self.user_data = None
        self.devices = []
        
    def build(self):
        # Set window size for mobile simulation
        Window.size = (360, 640)
        
        # Create screen manager
        self.sm = ScreenManager(transition=SlideTransition())
        
        # Add screens
        self.sm.add_widget(SplashScreen(name='splash'))
        self.sm.add_widget(LoginScreen(name='login'))
        self.sm.add_widget(RegisterScreen(name='register'))
        self.sm.add_widget(DashboardScreen(name='dashboard'))
        self.sm.add_widget(QRScannerScreen(name='qr_scanner'))
        self.sm.add_widget(DevicesScreen(name='devices'))
        self.sm.add_widget(ProfileScreen(name='profile'))
        
        return self.sm
    
    def show_snackbar(self, text, duration=3):
        """Show snackbar notification"""
        snackbar = Snackbar(duration=duration)
        snackbar.text = text
        snackbar.open()
    
    def show_dialog(self, title, text, callback=None):
        """Show dialog popup"""
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda x: (dialog.dismiss(), callback() if callback else None)
                )
            ]
        )
        dialog.open()


class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = MDFloatLayout()
        
        # Background gradient effect
        with layout.canvas.before:
            Color(0.4, 0.3, 0.7, 1)  # Deep purple
            self.rect = RoundedRectangle(size=layout.size, pos=layout.pos)
            layout.bind(size=self._update_rect, pos=self._update_rect)
        
        # Main card
        main_card = MDCard(
            size_hint=(0.9, 0.7),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            elevation=15,
            radius=[20, 20, 20, 20],
            md_bg_color=[1, 1, 1, 1]
        )
        
        card_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(20),
            padding=[dp(30), dp(40), dp(30), dp(40)]
        )
        
        # App logo and title
        logo_layout = MDBoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(120),
            spacing=dp(10)
        )
        
        logo = MDLabel(
            text="🔐",
            font_size=dp(48),
            halign="center",
            theme_text_color="Primary"
        )
        
        title = MDLabel(
            text="SecureLink",
            font_size=dp(28),
            font_name="Roboto-Bold",
            halign="center",
            theme_text_color="Primary"
        )
        
        subtitle = MDLabel(
            text="Secure QR Authentication",
            font_size=dp(14),
            halign="center",
            theme_text_color="Secondary"
        )
        
        logo_layout.add_widget(logo)
        logo_layout.add_widget(title)
        logo_layout.add_widget(subtitle)
        
        # Input fields
        self.username_field = MDTextField(
            hint_text="Username",
            icon_left="account",
            size_hint_y=None,
            height=dp(56),
            line_color_focus=self.theme_cls.primary_color
        )
        
        self.password_field = MDTextField(
            hint_text="Password",
            icon_left="lock",
            password=True,
            size_hint_y=None,
            height=dp(56),
            line_color_focus=self.theme_cls.primary_color
        )
        
        # Login button
        login_btn = MDRaisedButton(
            text="Login",
            size_hint_y=None,
            height=dp(48),
            md_bg_color=self.theme_cls.primary_color,
            on_release=self.login_user
        )
        
        # Register link
        register_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(40),
            spacing=dp(5)
        )
        
        register_label = MDLabel(
            text="Don't have an account?",
            font_size=dp(14),
            theme_text_color="Secondary",
            size_hint_x=None,
            width=dp(150)
        )
        
        register_btn = MDFlatButton(
            text="Register",
            theme_text_color="Primary",
            on_release=self.go_to_register
        )
        
        register_layout.add_widget(register_label)
        register_layout.add_widget(register_btn)
        
        # Add all widgets
        card_layout.add_widget(logo_layout)
        card_layout.add_widget(self.username_field)
        card_layout.add_widget(self.password_field)
        card_layout.add_widget(login_btn)
        card_layout.add_widget(register_layout)
        
        main_card.add_widget(card_layout)
        layout.add_widget(main_card)
        self.add_widget(layout)
    
    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos
    
    def login_user(self, instance):
        username = self.username_field.text
        password = self.password_field.text
        
        if not username or not password:
            self.app.show_snackbar("Please fill in all fields")
            return
        
        # Show loading
        self.show_loading(True)
        
        # Login in background thread
        threading.Thread(target=self._login_request, args=(username, password)).start()
    
    def _login_request(self, username, password):
        try:
            response = requests.post(
                f"{API_BASE_URL}/auth/login",
                json={"username": username, "password": password}
            )
            
            Clock.schedule_once(lambda dt: self.show_loading(False))
            
            if response.status_code == 200:
                data = response.json()
                app = MDApp.get_running_app()
                app.user_token = data['access_token']
                app.user_data = data['user']
                
                Clock.schedule_once(lambda dt: self._login_success())
            else:
                Clock.schedule_once(lambda dt: MDApp.get_running_app().show_snackbar("Invalid credentials"))
                
        except Exception as e:
            Clock.schedule_once(lambda dt: MDApp.get_running_app().show_snackbar(f"Connection error: {str(e)}"))
    
    def _login_success(self):
        app = MDApp.get_running_app()
        app.show_snackbar("Login successful!")
        app.sm.current = 'dashboard'
    
    def show_loading(self, show):
        # Implement loading state
        pass
    
    def go_to_register(self, instance):
        app = MDApp.get_running_app()
        app.sm.current = 'register'

class RegisterScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = MDFloatLayout()
        
        # Background
        with layout.canvas.before:
            Color(0.4, 0.3, 0.7, 1)
            self.rect = RoundedRectangle(size=layout.size, pos=layout.pos)
            layout.bind(size=self._update_rect, pos=self._update_rect)
        
        # Main card
        main_card = MDCard(
            size_hint=(0.9, 0.8),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            elevation=15,
            radius=[20, 20, 20, 20],
            md_bg_color=[1, 1, 1, 1]
        )
        
        card_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(20),
            padding=[dp(30), dp(40), dp(30), dp(40)]
        )
        
        # Title
        title = MDLabel(
            text="Create Account",
            font_size=dp(24),
            font_name="Roboto-Bold",
            halign="center",
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(40)
        )
        
        # Input fields
        self.username_field = MDTextField(
            hint_text="Username",
            icon_left="account",
            size_hint_y=None,
            height=dp(56)
        )
        
        self.email_field = MDTextField(
            hint_text="Email",
            icon_left="email",
            size_hint_y=None,
            height=dp(56)
        )
        
        self.password_field = MDTextField(
            hint_text="Password",
            icon_left="lock",
            password=True,
            size_hint_y=None,
            height=dp(56)
        )
        
        self.confirm_password_field = MDTextField(
            hint_text="Confirm Password",
            icon_left="lock-check",
            password=True,
            size_hint_y=None,
            height=dp(56)
        )
        
        # Register button
        register_btn = MDRaisedButton(
            text="Create Account",
            size_hint_y=None,
            height=dp(48),
            md_bg_color=self.theme_cls.primary_color,
            on_release=self.register_user
        )
        
        # Back to login
        back_btn = MDFlatButton(
            text="← Back to Login",
            theme_text_color="Primary",
            on_release=self.go_to_login
        )
        
        # Add widgets
        card_layout.add_widget(title)
        card_layout.add_widget(self.username_field)
        card_layout.add_widget(self.email_field)
        card_layout.add_widget(self.password_field)
        card_layout.add_widget(self.confirm_password_field)
        card_layout.add_widget(register_btn)
        card_layout.add_widget(back_btn)
        
        main_card.add_widget(card_layout)
        layout.add_widget(main_card)
        self.add_widget(layout)
    
    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos
    
    def register_user(self, instance):
        username = self.username_field.text
        email = self.email_field.text
        password = self.password_field.text
        confirm_password = self.confirm_password_field.text
        
        if not all([username, email, password, confirm_password]):
            app = MDApp.get_running_app()
            app.show_snackbar("Please fill in all fields")
            return
        
        if password != confirm_password:
            app = MDApp.get_running_app()
            app.show_snackbar("Passwords don't match")
            return
        
        # Register in background thread
        threading.Thread(target=self._register_request, args=(username, email, password)).start()
    
    def _register_request(self, username, email, password):
        try:
            response = requests.post(
                f"{API_BASE_URL}/auth/register",
                json={"username": username, "email": email, "password": password}
            )
            
            if response.status_code == 200:
                Clock.schedule_once(lambda dt: self._register_success())
            else:
                error_msg = response.json().get('detail', 'Registration failed')
                Clock.schedule_once(lambda dt: self._register_error(error_msg))
                
        except Exception as e:
            Clock.schedule_once(lambda dt: self._register_error(f"Connection error: {str(e)}"))
    
    def _register_success(self):
        app = MDApp.get_running_app()
        app.show_snackbar("Account created successfully!")
        app.sm.current = 'login'
    
    def _register_error(self, error_msg):
        app = MDApp.get_running_app()
        app.show_snackbar(error_msg)
    
    def go_to_login(self, instance):
        app = MDApp.get_running_app()
        app.sm.current = 'login'

class DashboardScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        # Bottom navigation
        self.bottom_nav = MDBottomNavigation(
            panel_color=self.theme_cls.primary_color,
            selected_color_background=self.theme_cls.primary_light,
            text_color_active=[1, 1, 1, 1]
        )
        
        # Home tab
        home_item = MDBottomNavigationItem(
            name='home',
            text='Home',
            icon='home'
        )
        home_item.add_widget(self.create_home_tab())
        
        # QR Scanner tab
        qr_item = MDBottomNavigationItem(
            name='qr',
            text='QR Scanner',
            icon='qrcode-scan'
        )
        qr_item.add_widget(self.create_qr_tab())
        
        # Devices tab
        devices_item = MDBottomNavigationItem(
            name='devices',
            text='Devices',
            icon='devices'
        )
        devices_item.add_widget(self.create_devices_tab())
        
        # Profile tab
        profile_item = MDBottomNavigationItem(
            name='profile',
            text='Profile',
            icon='account'
        )
        profile_item.add_widget(self.create_profile_tab())
        
        self.bottom_nav.add_widget(home_item)
        self.bottom_nav.add_widget(qr_item)
        self.bottom_nav.add_widget(devices_item)
        self.bottom_nav.add_widget(profile_item)
        
        self.add_widget(self.bottom_nav)
    
    def create_home_tab(self):
        scroll = ScrollView()
        layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(20),
            padding=[dp(20), dp(20), dp(20), dp(20)]
        )
        layout.bind(minimum_height=layout.setter('height'))
        
        # Welcome card
        welcome_card = MDCard(
            size_hint_y=None,
            height=dp(120),
            elevation=5,
            radius=[15, 15, 15, 15],
            md_bg_color=self.theme_cls.primary_color
        )
        
        welcome_layout = MDBoxLayout(
            orientation='vertical',
            padding=[dp(20), dp(20), dp(20), dp(20)],
            spacing=dp(10)
        )
        
        app = MDApp.get_running_app()
        username = app.user_data['username'] if app.user_data else "User"
        
        welcome_title = MDLabel(
            text=f"Welcome back, {username}! 👋",
            font_size=dp(20),
            font_name="Roboto-Bold",
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1]
        )
        
        welcome_subtitle = MDLabel(
            text="Secure device linking made simple",
            font_size=dp(14),
            theme_text_color="Custom",
            text_color=[1, 1, 1, 0.8]
        )
        
        welcome_layout.add_widget(welcome_title)
        welcome_layout.add_widget(welcome_subtitle)
        welcome_card.add_widget(welcome_layout)
        
        # Quick actions
        quick_actions_title = MDLabel(
            text="Quick Actions",
            font_size=dp(18),
            font_name="Roboto-Bold",
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(40)
        )
        
        # QR Scanner button
        qr_button = MDRaisedButton(
            text="📱 Scan QR Code",
            size_hint_y=None,
            height=dp(48),
            md_bg_color=self.theme_cls.accent_color,
            on_release=self.open_qr_scanner
        )
        
        # View devices button
        devices_button = MDRaisedButton(
            text="📱 My Devices",
            size_hint_y=None,
            height=dp(48),
            md_bg_color=self.theme_cls.primary_color,
            on_release=self.view_devices
        )
        
        layout.add_widget(welcome_card)
        layout.add_widget(quick_actions_title)
        layout.add_widget(qr_button)
        layout.add_widget(devices_button)
        
        scroll.add_widget(layout)
        return scroll
    
    def create_qr_tab(self):
        return QRScannerWidget()
    
    def create_devices_tab(self):
        return DevicesWidget()
    
    def create_profile_tab(self):
        return ProfileWidget()
    
    def open_qr_scanner(self, instance):
        # Switch to QR tab
        self.bottom_nav.switch_tab('qr')
    
    def view_devices(self, instance):
        # Switch to devices tab
        self.bottom_nav.switch_tab('devices')

class QRScannerWidget(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = dp(20)
        self.padding = [dp(20), dp(20), dp(20), dp(20)]
        self.scanning = False
        self.build_ui()
    
    def build_ui(self):
        # Title
        title = MDLabel(
            text="QR Code Scanner",
            font_size=dp(24),
            font_name="Roboto-Bold",
            theme_text_color="Primary",
            halign="center",
            size_hint_y=None,
            height=dp(40)
        )
        
        # Instructions
        instructions = MDLabel(
            text="Point your camera at a QR code to scan it and link a new device",
            font_size=dp(14),
            theme_text_color="Secondary",
            halign="center",
            text_size=(None, None),
            size_hint_y=None,
            height=dp(60)
        )
        instructions.bind(width=lambda *x: instructions.setter('text_size')(instructions, (instructions.width, None)))
        
        # Camera preview placeholder
        camera_card = MDCard(
            size_hint=(1, 0.6),
            elevation=10,
            radius=[15, 15, 15, 15],
            md_bg_color=[0.9, 0.9, 0.9, 1]
        )
        
        camera_layout = MDFloatLayout()
        
        camera_placeholder = MDLabel(
            text="📷\nCamera Preview\n\nTap 'Start Scanning' to begin",
            font_size=dp(16),
            theme_text_color="Secondary",
            halign="center",
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        camera_layout.add_widget(camera_placeholder)
        camera_card.add_widget(camera_layout)
        
        # Scan button
        self.scan_button = MDRaisedButton(
            text="Start Scanning",
            size_hint_y=None,
            height=dp(48),
            md_bg_color=self.theme_cls.primary_color,
            on_release=self.toggle_scanning
        )
        
        # Status label
        self.status_label = MDLabel(
            text="Ready to scan",
            font_size=dp(14),
            theme_text_color="Secondary",
            halign="center",
            size_hint_y=None,
            height=dp(30)
        )
        
        self.add_widget(title)
        self.add_widget(instructions)
        self.add_widget(camera_card)
        self.add_widget(self.scan_button)
        self.add_widget(self.status_label)
    
    def toggle_scanning(self, instance):
        if not self.scanning:
            self.start_scanning()
        else:
            self.stop_scanning()
    
    def start_scanning(self):
        self.scanning = True
        self.scan_button.text = "Stop Scanning"
        self.status_label.text = "Scanning for QR codes..."
        
        # Start camera scanning in background
        threading.Thread(target=self._scan_qr_codes, daemon=True).start()
    
    def stop_scanning(self):
        self.scanning = False
        self.scan_button.text = "Start Scanning"
        self.status_label.text = "Scanning stopped"
    
    def _scan_qr_codes(self):
        """
        Mock QR scanning - in a real implementation, this method would use
        the device's camera to capture and decode QR codes.
        """
        while self.scanning:
            time.sleep(2)
            # Simulate QR code detection
            Clock.schedule_once(lambda dt: self._mock_qr_detected())
            break
    
    def _mock_qr_detected(self):
        """Mock QR code detection for demo"""
        qr_data = {
            "session_id": "mock-session-123",
            "timestamp": datetime.now().isoformat(),
            "expires_at": (datetime.now()).isoformat()
        }
        
        self.process_qr_code(json.dumps(qr_data))
    
    def process_qr_code(self, qr_data_str):
        try:
            qr_data = json.loads(qr_data_str)
            session_id = qr_data.get('session_id')
            
            if session_id:
                self.status_label.text = "QR Code detected! Processing..."
                threading.Thread(target=self._link_device, args=(session_id,)).start()
            else:
                Clock.schedule_once(lambda dt: self._show_error("Invalid QR code"))
                
        except Exception as e:
            Clock.schedule_once(lambda dt: self._show_error(f"Error processing QR code: {str(e)}"))
    
    def _link_device(self, session_id):
        try:
            app = MDApp.get_running_app()
            headers = {"Authorization": f"Bearer {app.user_token}"}
            
            response = requests.post(
                f"{API_BASE_URL}/qr/scan",
                json={"session_id": session_id},
                headers=headers
            )
            
            if response.status_code == 200:
                Clock.schedule_once(lambda dt: self._link_success())
            else:
                error_msg = response.json().get('detail', 'Failed to link device')
                Clock.schedule_once(lambda dt: self._show_error(error_msg))
                
        except Exception as e:
            Clock.schedule_once(lambda dt: self._show_error(f"Connection error: {str(e)}"))
    
    def _link_success(self):
        self.stop_scanning()
        app = MDApp.get_running_app()
        app.show_snackbar("Device linked successfully! 🎉")
        self.status_label.text = "Device linked successfully!"
    
    def _show_error(self, error_msg):
        self.stop_scanning()
        app = MDApp.get_running_app()
        app.show_snackbar(error_msg)
        self.status_label.text = f"Error: {error_msg}"

class DevicesWidget(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = dp(20)
        self.padding = [dp(20), dp(20), dp(20), dp(20)]
        self.build_ui()
    
    def build_ui(self):
        # Title
        title = MDLabel(
            text="Linked Devices",
            font_size=dp(24),
            font_name="Roboto-Bold",
            theme_text_color="Primary",
            halign="center",
            size_hint_y=None,
            height=dp(40)
        )
        
        # Refresh button
        refresh_btn = MDRaisedButton(
            text="🔄 Refresh",
            size_hint_y=None,
            height=dp(48),
            md_bg_color=self.theme_cls.primary_color,
            on_release=self.refresh_devices
        )
        
        # Devices list
        self.devices_scroll = ScrollView()
        self.devices_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint_y=None
        )
        self.devices_layout.bind(minimum_height=self.devices_layout.setter('height'))
        
        self.devices_scroll.add_widget(self.devices_layout)
        
        self.add_widget(title)
        self.add_widget(refresh_btn)
        self.add_widget(self.devices_scroll)
    
    def refresh_devices(self, instance):
        threading.Thread(target=self._load_devices).start()
    
    def _load_devices(self):
        try:
            app = MDApp.get_running_app()
            headers = {"Authorization": f"Bearer {app.user_token}"}
            
            response = requests.get(f"{API_BASE_URL}/devices", headers=headers)
            
            if response.status_code == 200:
                devices = response.json()
                Clock.schedule_once(lambda dt: self._update_devices_ui(devices))
            else:
                Clock.schedule_once(lambda dt: MDApp.get_running_app().show_snackbar("Failed to load devices"))
                
        except Exception as e:
            Clock.schedule_once(lambda dt: MDApp.get_running_app().show_snackbar(f"Connection error: {str(e)}"))
    
    def _update_devices_ui(self, devices):
        self.devices_layout.clear_widgets()
        
        if not devices:
            no_devices = MDLabel(
                text="No linked devices found.\nScan a QR code to link your first device!",
                font_size=dp(16),
                theme_text_color="Secondary",
                halign="center",
                size_hint_y=None,
                height=dp(80)
            )
            self.devices_layout.add_widget(no_devices)
            return
        
        for device in devices:
            device_card = self.create_device_card(device)
            self.devices_layout.add_widget(device_card)
    
    def create_device_card(self, device):
        card = MDCard(
            size_hint_y=None,
            height=dp(120),
            elevation=5,
            radius=[10, 10, 10, 10],
            md_bg_color=[1, 1, 1, 1]
        )
        
        layout = MDBoxLayout(
            orientation='horizontal',
            padding=[dp(15), dp(15), dp(15), dp(15)],
            spacing=dp(15)
        )
        
        # Device info
        info_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(5)
        )
        
        device_name = MDLabel(
            text=device['device_name'],
            font_size=dp(16),
            font_name="Roboto-Bold",
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(25)
        )
        
        created_date = datetime.fromisoformat(device['created_at']).strftime("%B %d, %Y")
        device_date = MDLabel(
            text=f"Created: {created_date}",
            font_size=dp(12),
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(20)
        )
        
        status_text = "🟢 Active" if device['is_active'] else "🔴 Inactive"
        device_status = MDLabel(
            text=status_text,
            font_size=dp(12),
            theme_text_color="Primary" if device['is_active'] else "Error",
            size_hint_y=None,
            height=dp(20)
        )
        
        info_layout.add_widget(device_name)
        info_layout.add_widget(device_date)
        info_layout.add_widget(device_status)
        
        # Revoke button
        if device['is_active']:
            revoke_btn = MDRaisedButton(
                text="Revoke",
                size_hint=(None, None),
                size=(dp(80), dp(35)),
                md_bg_color=[0.8, 0.2, 0.2, 1],
                font_size=dp(12),
                on_release=lambda x, d=device: self.revoke_device(d['device_id'])
            )
        else:
            revoke_btn = MDLabel(
                text="Revoked",
                size_hint=(None, None),
                size=(dp(80), dp(35)),
                theme_text_color="Secondary"
            )
        
        layout.add_widget(info_layout)
        layout.add_widget(revoke_btn)
        card.add_widget(layout)
        
        return card
    
    def revoke_device(self, device_id):
        threading.Thread(target=self._revoke_device_request, args=(device_id,)).start()
    
    def _revoke_device_request(self, device_id):
        try:
            app = MDApp.get_running_app()
            headers = {"Authorization": f"Bearer {app.user_token}"}
            
            response = requests.delete(f"{API_BASE_URL}/devices/{device_id}", headers=headers)
            
            if response.status_code == 200:
                Clock.schedule_once(lambda dt: self._revoke_success())
            else:
                Clock.schedule_once(lambda dt: app.show_snackbar("Failed to revoke device"))
                
        except Exception as e:
            Clock.schedule_once(lambda dt: app.show_snackbar(f"Connection error: {str(e)}"))
    
    def _revoke_success(self):
        app = MDApp.get_running_app()
        app.show_snackbar("Device revoked successfully!")
        self.refresh_devices(None)

class ProfileWidget(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = dp(20)
        self.padding = [dp(20), dp(20), dp(20), dp(20)]
        self.build_ui()
    
    def build_ui(self):
        scroll = ScrollView()
        layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(20),
            size_hint_y=None
        )
        layout.bind(minimum_height=layout.setter('height'))
        
        app = MDApp.get_running_app()
        user_data = app.user_data
        
        # Profile header
        profile_card = MDCard(
            size_hint_y=None,
            height=dp(150),
            elevation=10,
            radius=[15, 15, 15, 15],
            md_bg_color=self.theme_cls.primary_color
        )
        
        profile_layout = MDBoxLayout(
            orientation='vertical',
            padding=[dp(20), dp(20), dp(20), dp(20)],
            spacing=dp(10)
        )
        
        # Avatar
        avatar = MDLabel(
            text="👤",
            font_size=dp(48),
            halign="center",
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
            size_hint_y=None,
            height=dp(60)
        )
        
        # User name
        username_label = MDLabel(
            text=user_data['username'] if user_data else "User",
            font_size=dp(20),
            font_name="Roboto-Bold",
            halign="center",
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
            size_hint_y=None,
            height=dp(30)
        )
        
        # Email
        email_label = MDLabel(
            text=user_data['email'] if user_data else "user@example.com",
            font_size=dp(14),
            halign="center",
            theme_text_color="Custom",
            text_color=[1, 1, 1, 0.8],
            size_hint_y=None,
            height=dp(25)
        )
        
        profile_layout.add_widget(avatar)
        profile_layout.add_widget(username_label)
        profile_layout.add_widget(email_label)
        profile_card.add_widget(profile_layout)
        
        # User stats
        stats_card = MDCard(
            size_hint_y=None,
            height=dp(100),
            elevation=5,
            radius=[15, 15, 15, 15],
            md_bg_color=[1, 1, 1, 1]
        )
        
        stats_layout = MDGridLayout(
            cols=2,
            padding=[dp(20), dp(20), dp(20), dp(20)],
            spacing=dp(20)
        )
        
        # Account created
        created_date = datetime.fromisoformat(user_data['created_at']).strftime("%B %Y") if user_data else "Unknown"
        created_stat = MDBoxLayout(orientation='vertical', spacing=dp(5))
        created_title = MDLabel(
            text="Member Since",
            font_size=dp(12),
            theme_text_color="Secondary",
            halign="center"
        )
        created_value = MDLabel(
            text=created_date,
            font_size=dp(16),
            font_name="Roboto-Bold",
            theme_text_color="Primary",
            halign="center"
        )
        created_stat.add_widget(created_title)
        created_stat.add_widget(created_value)
        
        # Account status
        status_stat = MDBoxLayout(orientation='vertical', spacing=dp(5))
        status_title = MDLabel(
            text="Account Status",
            font_size=dp(12),
            theme_text_color="Secondary",
            halign="center"
        )
        status_value = MDLabel(
            text="✅ Active",
            font_size=dp(16),
            font_name="Roboto-Bold",
            theme_text_color="Primary",
            halign="center"
        )
        status_stat.add_widget(status_title)
        status_stat.add_widget(status_value)
        
        stats_layout.add_widget(created_stat)
        stats_layout.add_widget(status_stat)
        stats_card.add_widget(stats_layout)
        
        # Action buttons
        actions_title = MDLabel(
            text="Account Actions",
            font_size=dp(18),
            font_name="Roboto-Bold",
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(40)
        )
        
        # Settings button
        settings_btn = MDRaisedButton(
            text="⚙️ Settings",
            size_hint_y=None,
            height=dp(48),
            md_bg_color=self.theme_cls.accent_color,
            on_release=self.open_settings
        )
        
        # Help button
        help_btn = MDRaisedButton(
            text="❓ Help & Support",
            size_hint_y=None,
            height=dp(48),
            md_bg_color=self.theme_cls.primary_color,
            on_release=self.open_help
        )
        
        # Logout button
        logout_btn = MDRaisedButton(
            text="🚪 Logout",
            size_hint_y=None,
            height=dp(48),
            md_bg_color=[0.8, 0.2, 0.2, 1],
            on_release=self.logout_user
        )
        
        # Security info
        security_card = MDCard(
            size_hint_y=None,
            height=dp(120),
            elevation=5,
            radius=[15, 15, 15, 15],
            md_bg_color=[0.9, 1, 0.9, 1]
        )
        
        security_layout = MDBoxLayout(
            orientation='vertical',
            padding=[dp(20), dp(15), dp(20), dp(15)],
            spacing=dp(10)
        )
        
        security_title = MDLabel(
            text="🔒 Security Notice",
            font_size=dp(16),
            font_name="Roboto-Bold",
            theme_text_color="Primary"
        )
        
        security_text = MDLabel(
            text="Your account is protected with secure QR authentication. Only scan QR codes from trusted sources.",
            font_size=dp(12),
            theme_text_color="Secondary",
            text_size=(None, None)
        )
        security_text.bind(width=lambda *x: security_text.setter('text_size')(security_text, (security_text.width, None)))
        
        security_layout.add_widget(security_title)
        security_layout.add_widget(security_text)
        security_card.add_widget(security_layout)
        
        # Add all widgets
        layout.add_widget(profile_card)
        layout.add_widget(stats_card)
        layout.add_widget(actions_title)
        layout.add_widget(settings_btn)
        layout.add_widget(help_btn)
        layout.add_widget(security_card)
        layout.add_widget(logout_btn)
        
        scroll.add_widget(layout)
        self.add_widget(scroll)
    
    def open_settings(self, instance):
        app = MDApp.get_running_app()
        app.show_snackbar("Settings feature coming soon!")
    
    def open_help(self, instance):
        app = MDApp.get_running_app()
        app.show_dialog(
            "Help & Support",
            "For support, please contact:\n\nsupport@securelink.app\n\nOr visit our website for documentation and tutorials."
        )
    
    def logout_user(self, instance):
        def confirm_logout():
            app = MDApp.get_running_app()
            app.user_token = None
            app.user_data = None
            app.show_snackbar("Logged out successfully")
            app.sm.current = 'login'
        
        app = MDApp.get_running_app()
        dialog = MDDialog(
            title="Confirm Logout",
            text="Are you sure you want to logout?",
            buttons=[
                MDFlatButton(
                    text="Cancel",
                    on_release=lambda x: dialog.dismiss()
                ),
                MDRaisedButton(
                    text="Logout",
                    md_bg_color=[0.8, 0.2, 0.2, 1],
                    on_release=lambda x: (dialog.dismiss(), confirm_logout())
                )
            ]
        )
        dialog.open()

# Additional screens for navigation
class QRScannerScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(QRScannerWidget())

class DevicesScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.devices_widget = DevicesWidget()
        self.add_widget(self.devices_widget)

    def on_enter(self, *args):
        self.devices_widget.refresh_devices(None)

class ProfileScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(ProfileWidget())

# Custom splash screen layout
class SplashScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = MDFloatLayout()
        
        # Background gradient
        with layout.canvas.before:
            Color(0.4, 0.3, 0.7, 1)
            self.rect = RoundedRectangle(size=layout.size, pos=layout.pos)
            layout.bind(size=self._update_rect, pos=self._update_rect)
        
        # Logo container
        logo_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(20),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(None, None),
            size=(dp(200), dp(200))
        )
        
        # Animated logo
        self.logo = MDLabel(
            text="🔐",
            font_size=dp(80),
            halign="center",
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
            opacity=0,
            size_hint_y=None,
            height=dp(100)
        )
        
        # App name
        app_name = MDLabel(
            text="SecureLink",
            font_size=dp(32),
            font_name="Roboto-Bold",
            halign="center",
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1],
            size_hint_y=None,
            height=dp(50)
        )
        
        # Tagline
        tagline = MDLabel(
            text="Secure QR Authentication",
            font_size=dp(16),
            halign="center",
            theme_text_color="Custom",
            text_color=[1, 1, 1, 0.8],
            size_hint_y=None,
            height=dp(30)
        )
        
        # Loading indicator
        loading = MDLabel(
            text="Loading...",
            font_size=dp(14),
            halign="center",
            theme_text_color="Custom",
            text_color=[1, 1, 1, 0.6],
            size_hint_y=None,
            height=dp(20)
        )
        
        logo_layout.add_widget(self.logo)
        logo_layout.add_widget(app_name)
        logo_layout.add_widget(tagline)
        logo_layout.add_widget(loading)
        
        layout.add_widget(logo_layout)
        self.add_widget(layout)
    
    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos
    
    def on_enter(self):
        # Beautiful entrance animation
        Clock.schedule_once(self.animate_logo, 0.5)
        Clock.schedule_once(self.go_to_login, 3)
    
    def animate_logo(self, dt):
        anim = Animation(opacity=1, duration=1) + Animation(font_size=dp(100), duration=0.5)
        anim.start(self.logo)
    
    def go_to_login(self, dt):
        app = MDApp.get_running_app()
        app.sm.current = 'login'

# Run the app
if __name__ == '__main__':
    SecureLinkApp().run()
