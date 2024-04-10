import customtkinter
from PIL import Image
import os
from tkinter.messagebox import askokcancel, showwarning

import database
import utils

customtkinter.set_appearance_mode("light")

class App(customtkinter.CTk):
    width = 900
    height = 600

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("App")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)

        # load and create background image
        current_path = os.path.dirname(os.path.realpath(__file__))
        self.bg_image = customtkinter.CTkImage(Image.open(current_path + "/static/bg_gradient.jpg"),
                                               size=(self.width, self.height))
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0)

        # create login frame
        self.login_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.login_frame.grid(row=0, column=0, sticky="ns")
        self.login_label = customtkinter.CTkLabel(self.login_frame, text="LOGIN",
                                                  font=customtkinter.CTkFont('Arial Black', size=30, weight="bold"))
        self.login_label.grid(row=0, column=0, padx=30, pady=(150, 15))
        self.username_entry = customtkinter.CTkEntry(self.login_frame, width=200, placeholder_text="username")
        self.username_entry.grid(row=1, column=0, padx=30, pady=(15, 15))
        self.password_entry = customtkinter.CTkEntry(self.login_frame, width=200, show="*", placeholder_text="password")
        self.password_entry.grid(row=2, column=0, padx=30, pady=(0, 15))
        self.login_button = customtkinter.CTkButton(self.login_frame, text="Login →", command=self.login_event, width=200)
        self.login_button.grid(row=3, column=0, padx=30, pady=(15, 15))
        self.signup_button = customtkinter.CTkButton(self.login_frame, text="Register", command=self.register_event, width=200)
        self.signup_button.grid(row=4, column=0, padx=30, pady=(0, 15))

        # create main frame (session window)
        self.insession_username = customtkinter.StringVar() # To store username in session
        
        self.main_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.session_flash_message_frame = customtkinter.CTkFrame(self.main_frame, corner_radius=0)
        
        self.message_flash_banner_in_session = customtkinter.CTkLabel(self.session_flash_message_frame, text=None, font=customtkinter.CTkFont('verdana', size=15, weight="bold"))
        self.message_flash_banner_in_session.pack(side='left', fill='x')
        self.message_flash_dismiss_banner_button = customtkinter.CTkButton(self.session_flash_message_frame, 
                                                                           text='x', corner_radius=0, 
                                                                           width=50, fg_color='transparent', border_width=0, 
                                                                           hover_color='light pink', font=customtkinter.CTkFont('verdana', size=15, weight="bold"),
                                                                           text_color='red', command=self.session_flash_message_frame.grid_forget)
        self.message_flash_dismiss_banner_button.pack(side='right', fill='x')

        self.main_label = customtkinter.CTkLabel(self.main_frame, text=None, font=customtkinter.CTkFont('Arial', size=35, weight="bold"),fg_color='#4A97CF')
        self.main_label.grid(row=1, column=0, padx=0, pady=0, sticky='we')
        

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "recent.png")), size=(500, 150))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))
        
        # create the home frame for most widgets
        self.home_frame_for_most_widgets = customtkinter.CTkFrame(self.main_frame)
        self.home_frame_for_most_widgets.grid(row=2, column=0, padx=0, pady=0, sticky='ns')

        # Create frame for theme button and logout button
        self.theme_logout_buttons_frame = customtkinter.CTkFrame(self.main_frame)
        self.theme_logout_buttons_frame.grid(row=3, column=0, padx=10, pady=40, sticky='nesw')


        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self.home_frame_for_most_widgets, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="n", pady=(45, 45), padx=(10, 0))
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text=None, 
                                                             compound="left", font=customtkinter.CTkFont('arial', size=18, weight="bold"),
                                                             text_color='green')
        self.navigation_frame_label.grid(row=0, column=0, padx=0, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Recent Expenses",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Edit income info",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Add expenses",
                                                      fg_color="transparent", text_color=("orange", "orange"), hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w", font=customtkinter.CTkFont('arial', 15, 'bold'), command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.frame_4_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Savings goal",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w", font=customtkinter.CTkFont('arial', 15, 'bold'), command=self.frame_4_button_event)
        self.frame_4_button.grid(row=4, column=0, sticky="ew")

        self.frame_5_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Tips 💡",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w", command=self.frame_5_button_event)
        self.frame_5_button.grid(row=5, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.theme_logout_buttons_frame, values=["Light", "Dark", "System"], corner_radius=10,
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.pack(side='right', padx=(0, 150), pady=10)

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self.home_frame_for_most_widgets, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)
        

        # create second frame
        self.second_frame = customtkinter.CTkFrame(self.home_frame_for_most_widgets, corner_radius=0, fg_color="transparent")
        self.edit_income_entry = customtkinter.CTkEntry(self.second_frame, width=200, placeholder_text="Edit income amount")
        self.edit_income_entry.grid(row=1, column=0, pady=(0, 5))
        self.entry_var = customtkinter.StringVar()
        self.edit_income_balance_entry = customtkinter.CTkEntry(self.second_frame, width=200, placeholder_text="Edit income balance", text_color='green', fg_color='light green', textvariable=self.entry_var)
        self.edit_income_balance_entry.grid(row=2, column=0, pady=(0, 5))
        self.edit_currency_entry = customtkinter.CTkEntry(self.second_frame, width=200, placeholder_text="Edit currency")
        self.edit_currency_entry.grid(row=3, column=0)
        self.savings_plan_entry_insession_edit = customtkinter.CTkComboBox(self.second_frame, width=200, values=['Weekly', 'Monthly'])
        self.savings_plan_entry_insession_edit.grid(row=4, column=0, pady=(5, 0))
        self.save_income_edit_data_button = customtkinter.CTkButton(self.second_frame, text="Update", command=self.update_income_data, width=100)
        self.save_income_edit_data_button.grid(row=5, column=0, pady=15)

        # create third frame
        self.third_frame = customtkinter.CTkFrame(self.home_frame_for_most_widgets, corner_radius=0, fg_color="transparent")
        self.description_entry = customtkinter.CTkEntry(self.third_frame, width=250, placeholder_text="Description")
        self.description_entry.grid(row=1, column=0, pady=(0, 5))
        self.expense_amount_entry = customtkinter.CTkEntry(self.third_frame, width=250, placeholder_text="Amount")
        self.expense_amount_entry.grid(row=2, column=0, pady=(0, 5))
        self.expense_category_entry = customtkinter.CTkComboBox(self.third_frame, width=250, values=['housing', 'food', 'transportation', 'entertainment'])
        self.expense_category_entry.set('-choose category-')
        self.expense_category_entry.grid(row=3, column=0, pady=(0, 5))
        self.date_entry = customtkinter.CTkEntry(self.third_frame, width=250, placeholder_text="Date")
        self.date_entry.grid(row=4, column=0, pady=(0, 5))
        self.add_expense_button = customtkinter.CTkButton(self.third_frame, text="Add", command=self.add_expense, width=100)
        self.add_expense_button.grid(row=5, column=0, pady=20)

        # Create fourth frame
        self.fourth_frame = customtkinter.CTkFrame(self.home_frame_for_most_widgets, corner_radius=0, fg_color="transparent")
        self.savings_amount_status_label = customtkinter.CTkLabel(self.fourth_frame, text=None, text_color='dark grey', font=customtkinter.CTkFont('arial', 24, 'bold'))
        self.savings_amount_status_label.grid(row=1, column=0, pady=(0, 0))
        self.saving_status_health_label = customtkinter.CTkLabel(self.fourth_frame, text=None, text_color='dark grey', font=customtkinter.CTkFont('arial', 20, 'bold'))
        self.saving_status_health_label.grid(row=2, column=0, pady=(0, 20))
        self.savings_goal_edit_entry = customtkinter.CTkEntry(self.fourth_frame, width=190, placeholder_text="Edit savings goal", font=customtkinter.CTkFont('arial', 18, 'bold'))
        self.savings_goal_edit_entry.grid(row=3, column=0, pady=(0, 20))
        self.savings_edit_save_button = customtkinter.CTkButton(self.fourth_frame, text="Save", command=self.save_savings_edits, width=80)
        self.savings_edit_save_button.grid(row=4, column=0, pady=(0, 40))


        # Create fifth frame
        self.fifth_frame = customtkinter.CTkFrame(self.home_frame_for_most_widgets, corner_radius=0, fg_color="transparent")
        self.tips_text = customtkinter.CTkTextbox(self.fifth_frame, width=400, fg_color='transparent', font=customtkinter.CTkFont('verdana', 16, 'bold', ))
        self.tips_text.insert('0.0', utils.tips_string)
        self.tips_text.grid(row=1, column=0, padx=10, sticky='nwse')

        # image labels
        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="", image=self.large_test_image)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=0, pady=10)
        self.second_frame_large_image_label = customtkinter.CTkLabel(self.second_frame, text="", image=customtkinter.CTkImage(Image.open(os.path.join(image_path, "edit_income.png")), size=(500, 150)))
        self.second_frame_large_image_label.grid(row=0, column=0, padx=0, pady=10)
        self.third_frame_large_image_label = customtkinter.CTkLabel(self.third_frame, text="", image=customtkinter.CTkImage(Image.open(os.path.join(image_path, "add_expense.png")), size=(500, 150)))
        self.third_frame_large_image_label.grid(row=0, column=0, padx=0, pady=(10, 0))
        self.fourth_frame_large_image_label = customtkinter.CTkLabel(self.fourth_frame, text="", image=customtkinter.CTkImage(Image.open(os.path.join(image_path, "savings.png")), size=(500, 150)))
        self.fourth_frame_large_image_label.grid(row=0, column=0, padx=0, pady=10)
        self.fifth_frame_large_image_label = customtkinter.CTkLabel(self.fifth_frame, text="", image=customtkinter.CTkImage(Image.open(os.path.join(image_path, "tips.png")), size=(500, 150)))
        self.fifth_frame_large_image_label.grid(row=0, column=0, padx=0, pady=10)

        # select default frame
        self.select_frame_by_name("home")

        self.back_button = customtkinter.CTkButton(self.theme_logout_buttons_frame, text="← LOGOUT", corner_radius=10, command=self.back_event)
        self.back_button.pack(side='left', padx=(150, 0), pady=10)

        # Create REGISTER frame
        self.register_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.register_frame.grid_columnconfigure(0, weight=1)
        self.register_main_label = customtkinter.CTkLabel(self.register_frame, text="REGISTER AS A USER", font=customtkinter.CTkFont('Arial', size=25, weight="bold"))
        self.register_main_label.grid(row=0, column=0, padx=30, pady=(30, 15))
        self.message_flash_banner = customtkinter.CTkLabel(self.register_frame, text=None, font=customtkinter.CTkFont('verdana', size=15, weight="bold"))
        self.register_entries_frame = customtkinter.CTkFrame(self.register_frame, corner_radius=20)
        self.register_entries_frame.grid(row=3, column=0, padx=30, pady=(15, 15))
        self.register_username_entry = customtkinter.CTkEntry(self.register_entries_frame, width=200, placeholder_text="username")
        self.register_username_entry.grid(row=1, column=0, padx=30, pady=(15, 15))
        self.register_password_entry = customtkinter.CTkEntry(self.register_entries_frame, width=200, show="*", placeholder_text="password")
        self.register_password_entry.grid(row=2, column=0, padx=30, pady=(0, 15))
        self.register_currency = customtkinter.CTkEntry(self.register_entries_frame, width=200, placeholder_text="currency")
        self.register_currency.grid(row=3, column=0, padx=30, pady=(0, 15))
        self.savings_plan_entry = customtkinter.CTkOptionMenu(self.register_entries_frame, width=200, values=["Weekly", "Monthly"])
        self.savings_plan_entry.grid(row=6, column=0, padx=30, pady=(0, 15))
        self.savings_plan_entry.set('--Select savings plan--')
        self.register_amount_entry = customtkinter.CTkEntry(self.register_entries_frame, width=200, placeholder_text="total income")
        self.register_amount_entry.grid(row=4, column=0, padx=30, pady=(0, 15))
        self.savings_goal_amount_entry = customtkinter.CTkEntry(self.register_entries_frame, width=200, placeholder_text="savings goal")
        self.savings_goal_amount_entry.grid(row=5, column=0, padx=30, pady=(0, 15))
        self.register_signup_button = customtkinter.CTkButton(self.register_entries_frame, text="Register", command=self.actually_register_user, width=200)
        self.register_signup_button.grid(row=7, column=0, padx=30, pady=(0, 15))
        self.register_frame_back_button = customtkinter.CTkButton(self.register_frame, text="← Back", command=self.back_event, width=200)
        self.register_frame_back_button.grid(row=4, column=0, padx=30, pady=(15, 15))

    def login_event(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.insession_username.set(username)
        if database.get_user(username, password) is not None:
            self.login_frame.grid_forget()  # remove login frame
            self.main_frame.grid(row=0, column=0, sticky="nsew", padx=100)  # show main frame
            self.personalize_session_update(username)
            return
        showwarning('BRO', 'Incorrect username or password')
    
    def personalize_session_update(self, insession_username):
        global currency, username, savings_plan, total_income, income_balance, savings_goal, savings_balance, savings_status
        tup = database.get_account(insession_username)
        username = tup[0]
        currency = tup[1]
        savings_plan = tup[2]
        total_income = tup[3]
        income_balance = tup[4]
        savings_goal = tup[5]
        savings_balance = tup[6]
        savings_status = tup[7]

        self.main_label.configure(text=f'Welcome, {username}')
        self.navigation_frame_label.configure(text=f"Income Balance\n{currency}{income_balance:.2f}")
        self.edit_income_entry.delete(0, 'end')
        self.edit_income_entry.insert(1, f"{currency}{total_income:.2f}")
        self.edit_currency_entry.delete(0, 'end')
        self.edit_currency_entry.insert(0, currency)
        self.edit_income_balance_entry.delete(0, 'end')
        self.edit_income_balance_entry.insert(0, f"{income_balance:.2f}")
        self.savings_plan_entry_insession_edit.set(savings_plan)
        self.entry_var.set(f"{currency}{income_balance:.2f}") 
        self.savings_amount_status_label.configure(text=f'Current savings is {currency}{savings_balance:.2f}')
        self.saving_status_health_label.configure(text=f'Savings status: {savings_status}')
        self.savings_goal_edit_entry.delete(0, 'end')
        self.savings_goal_edit_entry.insert(1, f'{currency}{savings_goal:.2f}')        

    def update_income_data(self):
        try: 
            float(self.edit_income_entry.get().replace(currency, ''))
            float(self.edit_income_balance_entry.get().replace(currency, ''))            
            if self.savings_plan_entry_insession_edit.get() == savings_plan and self.edit_income_entry.get().replace(currency, '') == \
                f'{total_income:.2f}' and self.edit_currency_entry.get() == \
                currency and self.entry_var.get().replace(currency, '') == f'{income_balance:.2f}':

                self.flash_message('It doesn\'t look like you have changed anything', message_type='warning')
                return
            database.update_account(username, 
                                    currency=self.edit_currency_entry.get(), 
                                    savings_plan=self.savings_plan_entry_insession_edit.get(), 
                                    total_income=self.edit_income_entry.get().replace(currency, '').replace(self.edit_currency_entry.get(), ''), 
                                    income_balance=self.edit_income_balance_entry.get().replace(self.edit_currency_entry.get(), '').replace(currency, ''), 
                                    savings_goal=savings_goal, savings_balance=savings_balance, savings_status=savings_status)
            self.personalize_session_update(username)
            self.flash_message(' The income records have been updated successfully ', message_type='success')
        except ValueError: self.flash_message('Income must should be numeric. Quit being an ass, provide the correct info', message_type='error')
        
    def add_expense(self):
        for field in self.description_entry, self.expense_amount_entry, self.date_entry:
            if not field.get():
                self.flash_message(' Please fill in all the fields ', message_type='warning')
                return
        try:
            float(self.expense_amount_entry.get())
            global income_balance
            if income_balance < float(self.expense_amount_entry.get()):
                self.flash_message(' Failed. You do not have enough balance, please top up ', message_type='error')
                return
            if askokcancel('Please confirm', 'Are you sure you want to add this expense?'):
                income_balance -= float(self.expense_amount_entry.get())
                database.update_income_balance(username, income_balance)
                database.add_expense(username, self.description_entry.get(), self.expense_category_entry.get(), self.expense_amount_entry.get(), self.date_entry.get())
                self.personalize_session_update(self.insession_username.get())
                self.flash_message(' New expense has been added successfully ', message_type='success')
                return
            self.flash_message(' It looks you have cancelled the last operation ', message_type='warning')
        except ValueError: self.flash_message(' You must enter a numeric value for Amount ', message_type='error')

    def register_event(self):
        print("Register pressed - username")
        self.login_frame.grid_forget()  # remove login frame
        self.register_frame.grid(row=0, column=0, sticky="nsew", padx=100)  # show register frame
    
    def save_savings_edits(self):
        try:
            float(self.savings_goal_edit_entry.get().replace(currency, ''))
            if f'{self.savings_goal_edit_entry.get().replace(currency, '')}' == f'{savings_goal:.2f}':
                self.flash_message('It doesn\'t look like you have changed anything 🌚', message_type='warning')
                return
            database.update_savings_goal_amount(username, float(self.savings_goal_edit_entry.get().replace(currency, '')))
            database.update_saving_status(username, self.savings_goal_edit_entry.get().replace(currency, ''))
            self.personalize_session_update(username)
            self.flash_message('Success, you have edited the entered values successfully!', message_type='success')       
        except ValueError: self.flash_message('Error! You have to enter a numeric value for savings goal and amount', message_type='error')

    def back_event(self):
        self.insession_username.set('') # Reset session
        self.edit_income_entry.delete(0, 'end')

        self.main_frame.grid_forget()  # remove main frame is it is on grid
        self.register_frame.grid_forget() # remove register frame is it is on grid
        self.session_flash_message_frame.grid_forget() # destroy all flashed messages
        self.login_frame.grid(row=0, column=0, sticky="ns")  # show login frame
    
    def flash_message(self, message_text, message_type):
        """
        Supported message types:
        - 'success'
        - 'warning
        - 'error'
        """
        # TODO: flash the banner on row=1
        self.message_types_configuration = {
            'success': {'text': 'green', 'background': 'light blue'},
            'warning': {'text': 'orange', 'background': 'light yellow'},
            'error': {'text': 'red', 'background': 'light pink'},
        }
        self.message_flash_banner.configure(text=message_text, 
                                            text_color=self.message_types_configuration.get(message_type)['text'], 
                                            fg_color=self.message_types_configuration.get(message_type)['background'])
        self.message_flash_banner.grid(row=1, column=0, padx=0, pady=0, sticky='we')

        # TODO: GET RID OF UNNECESSARY CALL FOR OUTER BANNER
        self.message_flash_banner_in_session.configure(text=message_text, 
                                            text_color=self.message_types_configuration.get(message_type)['text'], 
                                            fg_color=self.message_types_configuration.get(message_type)['background'])
        self.session_flash_message_frame.grid(row=0, column=0, sticky='we')
        self.session_flash_message_frame.configure(fg_color=self.message_flash_banner_in_session._fg_color)
        self.message_flash_dismiss_banner_button.configure(text_color=self.message_flash_banner_in_session._text_color)
  
    def actually_register_user(self):
        print('Collecting registration data...')
        entries = [
            self.register_username_entry,
            self.register_password_entry,
            self.register_currency,
            self.savings_goal_amount_entry,
            self.register_amount_entry
        ]

        for entry in entries: # Check if any of the input fields is blank
            if not entry.get() or self.savings_plan_entry.get() == '--Select savings plan--':
                self.flash_message('Failed. Do not leave any field blank!', message_type='warning')
                return # Exit function

        try: # Check if amount is numeric
            # float(self.register_currency.get())
            float(self.register_amount_entry.get())
            if askokcancel('Everything looks set', 'The data looks correct. Do you wish to proceed?'):
                # Implement CRUD
                database_response = database.create_user(self.register_username_entry.get(), self.register_password_entry.get())
                message = database_response['message']
                if database_response.get('is_successful'):
                    message_type = 'success'      
                    database.create_account(self.register_username_entry.get(), self.register_currency.get(), 
                                            self.savings_plan_entry.get(), self.register_amount_entry.get(), 
                                            self.register_amount_entry.get(), self.savings_goal_amount_entry.get(), 
                                            5000, "Not set")

                else:
                    message_type = 'error'
                self.flash_message(message, message_type=message_type)
                return
            self.flash_message('You have cancelled this operation', message_type='warning')
            
        except ValueError:
            self.flash_message('Failed. You must enter numeric values for currency and amount.', message_type='error')
    
    # IN SESSION METHODS:
    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")
        self.frame_4_button.configure(fg_color=("gray75", "gray25") if name == "frame_4" else "transparent")
        self.frame_5_button.configure(fg_color=("gray75", "gray25") if name == "frame_5" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="n")

        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="n")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="n")
        else:
            self.third_frame.grid_forget()
        if name == "frame_4":
            self.fourth_frame.grid(row=0, column=1, sticky="n")
        else:
            self.fourth_frame.grid_forget()
        if name == "frame_5":
            self.fifth_frame.grid(row=0, column=1, sticky="n")
        else:
            self.fifth_frame.grid_forget()
        
    def home_button_event(self):
        self.select_frame_by_name("home")

        import ttkbootstrap as ttk
        from ttkbootstrap.tableview import Tableview
        from ttkbootstrap.constants import PRIMARY

        self.column_data = [
            {'text': 'ID', 'stretch': False, 'width': 145},
            {'text': 'Description', 'stretch': False, 'width': 145},
            {'text': 'Category', 'stretch': False, 'width': 145},
            {'text': f'Amount ({currency})', 'stretch': False, 'width': 145},
            {'text': 'Date', 'stretch': False, 'width': 145},
        ]
        self.rowdata = database.fetch_recent_expenses(self.insession_username.get())

        self.table_view = Tableview(
            self.home_frame,
            paginated=True,
            searchable=True,
            bootstyle=PRIMARY,
            coldata=self.column_data,
            rowdata=self.rowdata,
            stripecolor=('blue', 'light blue'),
        )
        self.table_view.grid(row=1, column=0, sticky='nwse', padx=10, pady=10)



    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")
        self.date_entry.delete(0, 'end')
        self.date_entry.insert(1, utils.CustomCalendar.date_today())
    
    def frame_4_button_event(self):
        self.select_frame_by_name("frame_4")
    
    def frame_5_button_event(self):
        self.select_frame_by_name("frame_5")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

if __name__ == "__main__":
    app = App()
    app.mainloop()
