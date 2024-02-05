import customtkinter as ctk
import tkinter as tk
import data_manager as data_mg
from functools import partial
import sales_calculator
import datetime

# ---------------------------------------------------------------------------------------------------------------- #
# global list
# ---------------------------------------------------------------------------------------------------------------- #
date_and_time = datetime.datetime.now()
dates = date_and_time.date()
times = date_and_time.strftime("%I:%M:%S %p")
date = str(dates)
time = str(times)
date_time = 'DATE | ' + date + ' TIME | ' + time

_discounted_items_listed = []
_order_listed = []
_return_list = []

ctk.set_default_color_theme('Themes/delta4.txt')
# ---------------------------------------------------------------------------------------------------------------- #
# window to for exceptions
# ---------------------------------------------------------------------------------------------------------------- #

class MenuGuide(ctk.CTkToplevel):

    def __init__(self):
        super().__init__()

        mg_frame = ctk.CTkFrame(self)
        mg_frame.pack()
        mg_button = ctk.CTkButton(mg_frame, command=partial(self.change))
        mg_button.grid(padx=100, pady=10)

    def change(self):
        global theme_number
        if theme_number > 4:
            theme_number = 0
        else:
            theme_number +=1
        app = POSApp()
        app.refresher()

# ---------------------------------------------------------------------------------------------------------------- #
# window to for exceptions
# ---------------------------------------------------------------------------------------------------------------- #

class Exceptions(ctk.CTkToplevel):
    def __init__(self, text_for_message):
        super().__init__()
        self.exception_message = text_for_message

        self.exceptions_window = ctk.CTkFrame(self)
        self.exceptions_window.pack()

        self.exception_label = ctk.CTkLabel(self.exceptions_window,
                                            text=self.exception_message, width=400, height=80)
        self.exception_label.grid(row=0, padx=10, pady=10)

        self.exception_button = ctk.CTkButton(self.exceptions_window,
                                              
                                              
                                              text=" OK ",
                                              command=partial(self.close_window)
                                              )
        self.exception_button.grid(row=1, padx=10, pady=10)


    def close_window(self):
        Exceptions.destroy(self)


# ---------------------------------------------------------------------------------------------------------------- #
# window to for credit
# ---------------------------------------------------------------------------------------------------------------- #

class ApplyCredit(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.credit = 0
        self._credit_font = ctk.CTkFont(family="Helvetica", size=16)

        self.credit_window = ctk.CTkFrame(self)
        self.credit_window.pack(padx=10, pady=10)

        self.credit_label = ctk.CTkLabel(self.credit_window,
                                         width=400,
                                         
                                         font=self._credit_font,
                                         
                                         text=' Only One Discount can be applied per order '
                                         )
        self.credit_label.grid(row=0, column=0, columnspan=4, padx=7, pady=10)

        self.button_credit_5 = ctk.CTkButton(self.credit_window,
                                             width=80,
                                             height=60,
                                             
                                             
                                             text=' $5 ',
                                             font=self._credit_font,
                                             command=partial(self.set_credit, 5)
                                             )
        self.button_credit_5.grid(row=1, column=0, padx=7, pady=10)

        self.button_credit_10 = ctk.CTkButton(self.credit_window,
                                             width=80,
                                             height=60,
                                             
                                             
                                             text=' $10 ',
                                             font=self._credit_font,
                                             command=partial(self.set_credit, 10)
                                             )
        self.button_credit_10.grid(row=1, column=1, padx=7, pady=10)

        self.button_credit_15 = ctk.CTkButton(self.credit_window,
                                              width=80,
                                              height=60,
                                              
                                              
                                              text=' $15 ',
                                              font=self._credit_font,
                                              command=partial(self.set_credit, 15)
                                              )
        self.button_credit_15.grid(row=1, column=2, padx=7, pady=10)

        self.button_credit_20 = ctk.CTkButton(self.credit_window,
                                              width=80,
                                              height=60,
                                              
                                              
                                              text=' $20 ',
                                              font=self._credit_font,
                                              command=partial(self.set_credit, 20)
                                              )
        self.button_credit_20.grid(row=1, column=3, padx=7, pady=10)
        self.grab_set()
        
    def set_credit(self, credit_amount):
        total_check, tex_pass, sub_pass = sales_calculator.totaler(_order_listed, 0, 0)
        if total_check >= credit_amount:
            self.credit = credit_amount
            print(self.credit)
            ApplyCredit.destroy(self)
        else:
            credit_exception1 = "Can't apply a credit greater than the total "
            pop_up = Exceptions(credit_exception1)
            self.credit = 0
            self.wait_window(pop_up)

# ---------------------------------------------------------------------------------------------------------------- #
# window to for discounts
# ---------------------------------------------------------------------------------------------------------------- #


class ApplyDiscount(ctk.CTkToplevel):
    global _discounted_items_listed


    def __init__(self):
        super().__init__()
        self.discount_amount_item = None
        self.item_discount_amount = ''
        self.item_discount_percentage = None
        self.discount_selection_items = None
        self.item_label = None
        self.labels_of_items = None
        self.selection_box = None
        self.discount_item_frame = None
        self.discount_amount = None
        self.percentage_holder = ''
        self.discount_submit = None
        self.custom_entry_frame = None
        self.custom_entry_label = None
        self.custom_entry = None
        self._75_percent_button = None
        self._65_percent_button = None
        self._50_percent_button = None
        self._30_percent_button = None
        self._25_percent_button = None
        self._20_percent_button = None
        self._10_percent_button = None
        self._100_percent_button = None
        self._5_percent_button = None
        self.order_current_total_window = None
        self.order_discount_frame = None
        self.title("Discount Window")
        self._discount_font = ctk.CTkFont(family="Helvetica", size=16)
        self._discount_total_font = ctk.CTkFont(family="Helvetica", size=20)

        self.order_or_item_frame = ctk.CTkFrame(self)
        self.order_or_item_frame.pack(pady=10, padx=10)

        self.selction_label = ctk.CTkLabel(self.order_or_item_frame,
                                           width=450,
                                           height=30,
                                           
                                           
                                           text=' Select to apply the discount to the order or an item ',
                                           font=self._discount_font
                                           )
        self.selction_label.grid(row=0, column=0, columnspan=2, pady=15, padx=15)

        self.order_button_select = ctk.CTkButton(self.order_or_item_frame,
                                                 width=100,
                                                 height=60,
                                                 
                                                 
                                                 text=' Apply discount to order ',
                                                 font=self._discount_font,
                                                 command=partial(self.new_frames_discount_order)
                                                 )
        self.order_button_select.grid(row=1, column=0, pady=15, padx=15)

        self.item_button_select = ctk.CTkButton(self.order_or_item_frame,
                                                width=100,
                                                height=60,
                                                
                                                
                                                text=' Apply discount to item ',
                                                font=self._discount_font,
                                                command=partial(self.new_frame_discount_items)
                                                )
        self.item_button_select.grid(row=1, column=1, pady=15, padx=15)
        self.discount_amount = 0
        self.grab_set()

    #------------------------------------------------------------------------------------------------------------------#
    # discount order
    # -----------------------------------------------------------------------------------------------------------------#

    def new_frames_discount_order(self):
        self.order_or_item_frame.destroy()
        self.order_discount_frame = ctk.CTkFrame(self)
        self.order_discount_frame.pack(pady=10, padx=10)
        order_total_float, order_tax_float, order_sub_total_float \
            = sales_calculator.totaler(_order_listed, 0, 0)
        order_total_formated = '{:.2f}'.format(order_total_float)
        order_tax_formated = '{:.2f}'.format(order_tax_float)
        order_sub_total_formated = '{:.2f}'.format(order_sub_total_float)
        order_total = str(order_total_formated)
        order_tax = str(order_tax_formated)
        order_sub_total = str(order_sub_total_formated)
        text_of_total = (" Total  $" + order_total
                         + "   |   Tax   $" + order_tax
                         + "   |   Subtotal       $" + order_sub_total
                         )
        self.order_current_total_window = ctk.CTkTextbox(self.order_discount_frame,
                                                         
                                                         
                                                         font=self._discount_total_font,
                                                         height=80,
                                                         width=510,
                                                         state='disabled'
                                                         )
        self.order_current_total_window.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        self.order_current_total_window.configure(state='normal')
        self.order_current_total_window.insert(1.0, text_of_total)
        self.order_current_total_window.configure(state='disabled')
        self._5_percent_button = ctk.CTkButton(self.order_discount_frame,
                                               width=150,
                                               height=60,
                                               
                                               
                                               text=' 5% Discount ',
                                               font=self._discount_font,
                                               command=partial(self.set_percentage_for_order, '5')
                                               )
        self._5_percent_button.grid(row=1, column=0, padx=10, pady=10)

        self._10_percent_button = ctk.CTkButton(self.order_discount_frame,
                                                width=150,
                                                height=60,
                                                
                                                
                                                text=' 10% Discount ',
                                                font=self._discount_font,
                                                command=partial(self.set_percentage_for_order, '10')
                                                )
        self._10_percent_button.grid(row=1, column=1, padx=10, pady=10)

        self._20_percent_button = ctk.CTkButton(self.order_discount_frame,
                                                width=150,
                                                height=60,
                                                
                                                
                                                text=' 20% Discount ',
                                                font=self._discount_font,
                                                command=partial(self.set_percentage_for_order, '20')
                                                )
        self._20_percent_button.grid(row=1, column=2, padx=10, pady=10)
        self._25_percent_button = ctk.CTkButton(self.order_discount_frame,
                                                width=150,
                                                height=60,
                                                
                                                
                                                text=' 25% Discount ',
                                                font=self._discount_font,
                                                command=partial(self.set_percentage_for_order, '25')
                                                )
        self._25_percent_button.grid(row=2, column=0, padx=10, pady=10)

        self._30_percent_button = ctk.CTkButton(self.order_discount_frame,
                                                width=150,
                                                height=60,
                                                
                                                
                                                text=' 30% Discount ',
                                                font=self._discount_font,
                                                command=partial(self.set_percentage_for_order, '30')
                                                )
        self._30_percent_button.grid(row=2, column=1, padx=10, pady=10)

        self._50_percent_button = ctk.CTkButton(self.order_discount_frame,
                                                width=150,
                                                height=60,
                                                
                                                
                                                text=' 50% Discount ',
                                                font=self._discount_font,
                                                command=partial(self.set_percentage_for_order, '50')
                                                )
        self._50_percent_button.grid(row=2, column=2, padx=10, pady=10)

        self._65_percent_button = ctk.CTkButton(self.order_discount_frame,
                                                width=150,
                                                height=60,
                                                
                                                
                                                text=' 65% Discount ',
                                                font=self._discount_font,
                                                command=partial(self.set_percentage_for_order, '65')
                                                )
        self._65_percent_button.grid(row=3, column=0, padx=10, pady=10)

        self._75_percent_button = ctk.CTkButton(self.order_discount_frame,
                                                width=150,
                                                height=60,
                                                
                                                
                                                text=' 75% Discount ',
                                                font=self._discount_font,
                                                command=partial(self.set_percentage_for_order, '75')
                                                )
        self._75_percent_button.grid(row=3, column=1, padx=10, pady=10)

        self._100_percent_button = ctk.CTkButton(self.order_discount_frame,
                                                 width=150,
                                                 height=60,
                                                 
                                                 
                                                 text=' 100% Discount ',
                                                 font=self._discount_font,
                                                 command=partial(self.set_percentage_for_order, '100')
                                                 )
        self._100_percent_button.grid(row=3, column=2, padx=10, pady=10)

        self.custom_entry_frame = ctk.CTkFrame(self.order_discount_frame,
                                               width=510,
                                               height=80)
        self.custom_entry_frame.grid(row=4, column=0, columnspan=3, padx=10, pady=10)
        user_input = tk.StringVar()
        self.custom_entry_label = ctk.CTkLabel(self.custom_entry_frame,
                                               width=300,
                                               height=60,
                                               text=' Enter a number between 1 - 100 ',
                                               font=self._discount_font
                                               )
        self.custom_entry_label.grid(row=0, column=0, padx=10, pady=10)
        self.custom_entry = ctk.CTkEntry(self.custom_entry_label, height=40, width=100,
                                          textvariable=user_input
                                         )
        self.custom_entry.grid(row=0, column=1, padx=10, pady=10)
        self.discount_submit = ctk.CTkButton(self.order_discount_frame,
                                             width=150,
                                             height=60,
                                             text=' Apply Discount ',
                                             font=self._discount_font,
                                             command=partial(self.apply_discount_to_order)
                                             )
        self.discount_submit.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

        self.grab_set()

    def set_percentage_for_order(self, percentage):
        self.percentage_holder = percentage
        self.discount_amount = 0

    def apply_discount_to_order(self):
        if self.percentage_holder != '':
            self.discount_amount = int(self.percentage_holder)
            self.destroy()
        elif self.percentage_holder == '':
            try:
                self.percentage_holder = int(self.custom_entry.get())
                if self.percentage_holder >= 101:
                    discount_exception1 = "Can't apply a discount over %100, \n please "
                    pop_up = Exceptions(discount_exception1)
                    self.wait_window(pop_up)
                    self.percentage_holder = 0
                else:
                    self.discount_amount = int(self.percentage_holder)
                    self.destroy()
            except ValueError:
                discount_exception2 = "Invalid entry, please enter a number between 1 - 100 "
                pop_up = Exceptions(discount_exception2)
                self.wait_window(pop_up)
                self.percentage_holder = 0
                self.discount_amount = 0
    #------------------------------------------------------------------------------------------------------------------#
    # discount item
    #------------------------------------------------------------------------------------------------------------------#

    def new_frame_discount_items(self):
        self.order_or_item_frame.destroy()
        self.discount_item_frame = ctk.CTkScrollableFrame(self, width=310, height=400)
        self.discount_item_frame.pack(padx=10, pady=10, side='left')
        item_rows = 0
        for items_for_discount in _order_listed:
            yes_or_no = tk.IntVar()
            item_rows += 1
            items_in_label = ('Item #:' + str(items_for_discount[4]) + '    Cost $' + items_for_discount[1] +
                              '\n' + items_for_discount[0])
            self.item_label = ctk.CTkFrame(self.discount_item_frame, width=300)
            self.item_label.grid(row=item_rows, column=0, padx=3, pady=3, sticky='nsew',)

            self.labels_of_items = ctk.CTkLabel(self.item_label,
                                                font=self._discount_font,
                                                height=80,
                                                width=245,
                                                justify='left',
                                                text=items_in_label)
            self.labels_of_items.grid(row=0, rowspan=3, column=0, padx=2, pady=2)
            self.labels_of_items.configure(state='normal')
            self.selection_box = ctk.CTkCheckBox(self.item_label,
                                                 text="      ", width=45,
                                                 onvalue=1, offvalue=0, variable=yes_or_no,
                                                 command=partial(self.discount_item_check, items_for_discount[4],
                                                                 yes_or_no)
                                                 )
            self.selection_box.grid(row=1, column=1, padx=3, pady=3, sticky='nsew')

        self.discount_selection_items = ctk.CTkFrame(self)
        self.discount_selection_items.pack(padx=10, pady=10, side='right')

        self._5_percent_button = ctk.CTkButton(self.discount_selection_items,
                                               width=150,
                                               height=60,
                                               
                                               
                                               text=' 5% Discount ',
                                               font=self._discount_font,
                                               command=partial(self.set_percentage_for_items, '5')
                                               )
        self._5_percent_button.grid(row=1, column=0, padx=10, pady=10)

        self._10_percent_button = ctk.CTkButton(self.discount_selection_items,
                                                width=150,
                                                height=60,
                                                
                                                
                                                text=' 10% Discount ',
                                                font=self._discount_font,
                                                command=partial(self.set_percentage_for_items, '10')
                                                )
        self._10_percent_button.grid(row=1, column=1, padx=10, pady=10)

        self._20_percent_button = ctk.CTkButton(self.discount_selection_items,
                                                width=150,
                                                height=60,
                                                
                                                
                                                text=' 20% Discount ',
                                                font=self._discount_font,
                                                command=partial(self.set_percentage_for_items, '20')
                                                )
        self._20_percent_button.grid(row=1, column=2, padx=10, pady=10)
        self._25_percent_button = ctk.CTkButton(self.discount_selection_items,
                                                width=150,
                                                height=60,
                                                
                                                
                                                text=' 25% Discount ',
                                                font=self._discount_font,
                                                command=partial(self.set_percentage_for_items, '25')
                                                )
        self._25_percent_button.grid(row=2, column=0, padx=10, pady=10)

        self._30_percent_button = ctk.CTkButton(self.discount_selection_items,
                                                width=150,
                                                height=60,
                                                
                                                
                                                text=' 30% Discount ',
                                                font=self._discount_font,
                                                command=partial(self.set_percentage_for_items, '30')
                                                )
        self._30_percent_button.grid(row=2, column=1, padx=10, pady=10)

        self._50_percent_button = ctk.CTkButton(self.discount_selection_items,
                                                width=150,
                                                height=60,
                                                
                                                
                                                text=' 50% Discount ',
                                                font=self._discount_font,
                                                command=partial(self.set_percentage_for_items, '50')
                                                )
        self._50_percent_button.grid(row=2, column=2, padx=10, pady=10)

        self._65_percent_button = ctk.CTkButton(self.discount_selection_items,
                                                width=150,
                                                height=60,
                                                
                                                
                                                text=' 65% Discount ',
                                                font=self._discount_font,
                                                command=partial(self.set_percentage_for_items, '65')
                                                )
        self._65_percent_button.grid(row=3, column=0, padx=10, pady=10)

        self._75_percent_button = ctk.CTkButton(self.discount_selection_items,
                                                width=150,
                                                height=60,
                                                
                                                
                                                text=' 75% Discount ',
                                                font=self._discount_font,
                                                command=partial(self.set_percentage_for_items, '75')
                                                )
        self._75_percent_button.grid(row=3, column=1, padx=10, pady=10)

        self._100_percent_button = ctk.CTkButton(self.discount_selection_items,
                                                 width=150,
                                                 height=60,
                                                 
                                                 
                                                 text=' 100% Discount ',
                                                 font=self._discount_font,
                                                 command=partial(self.set_percentage_for_items, '100')
                                                 )
        self._100_percent_button.grid(row=3, column=2, padx=10, pady=10)

        self.custom_entry_frame = ctk.CTkFrame(self.discount_selection_items,
                                               width=510,
                                               height=80)
        self.custom_entry_frame.grid(row=4, column=0, columnspan=3, padx=10, pady=10)
        user_input = tk.StringVar()
        self.custom_entry_label = ctk.CTkLabel(self.custom_entry_frame,
                                               width=300,
                                               height=60,
                                               text=' Enter a number between 1 - 100 ',
                                               font=self._discount_font
                                               )
        self.custom_entry_label.grid(row=0, column=0, padx=10, pady=10)
        self.custom_entry = ctk.CTkEntry(self.custom_entry_label, height=40, width=100,
                                          textvariable=user_input
                                         )
        self.custom_entry.grid(row=0, column=1, padx=10, pady=10)
        self.discount_submit = ctk.CTkButton(self.discount_selection_items,
                                             width=150,
                                             height=60,
                                             text=' Apply Discount ',
                                             font=self._discount_font,
                                             command=partial(self.selected_discount)
                                             )
        self.discount_submit.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

        self.grab_set()

    def set_percentage_for_items(self, percentage):
        self.item_discount_amount = percentage

    def discount_item_check(self, item_discounted, yes_no):
        if yes_no.get() == 1:
            _discounted_items_listed.append(item_discounted)
        else:
            _discounted_items_listed.remove(item_discounted)

    def selected_discount(self):
        if self.item_discount_amount != '':
            self.discount_amount_item = int(self.item_discount_amount)
            self.destroy()
        elif self.item_discount_amount == '':
            try:
                self.item_discount_amount = int(self.custom_entry.get())
                if self.item_discount_amount >= 101:
                    discount_exception3 = "Can't apply a discount over %100, \n please "
                    pop_up = Exceptions(discount_exception3)
                    self.wait_window(pop_up)
                else:
                    self.discount_amount_item = int(self.item_discount_amount)
                    self.destroy()
            except ValueError:
                self.discount_amount_item = 0
                discount_exception4 = " Invalid entry, please enter a number between 1 - 100 "
                pop_up = Exceptions(discount_exception4)
                self.wait_window(pop_up)

# ---------------------------------------------------------------------------------------------------------------- #
# window to remove items
# ---------------------------------------------------------------------------------------------------------------- #


class RemoveItems(ctk.CTkToplevel):

    ctk.set_appearance_mode("dark")

    def __init__(self):
        super().__init__()
        self.title("Remove Items Window")
        self._return_font = ctk.CTkFont(family="Helvetica", size=16)
        self.retun_window_label = ctk.CTkLabel(self,
                                               width=320,
  
                                               
                                               font=self._return_font,
                                               text="Select items to be removed"
                                               )
        self.retun_window_label.pack(padx=10, pady=7)
        self.remove_frame = ctk.CTkScrollableFrame(self, height=380, width=380)
        self.remove_frame.pack(padx=10, pady=10)
        rows_listed = 0
        for items_in_order in _order_listed:
            on_or_off = tk.IntVar()
            rows_listed += 1
            text_in_label = ('Item #:' + str(items_in_order[4]) + '    Cost $' + items_in_order[1] +
                             '\n' + items_in_order[0])
            self.item_label = ctk.CTkFrame(self.remove_frame, width=300)
            self.item_label.grid(row=rows_listed, padx=10, pady=10, sticky='nsew',)

            self.labels_from_list = ctk.CTkLabel(self.item_label,
                                                 font=self._return_font,
                                                 text=text_in_label,
                                                 height=80,
                                                 width=245,
                                                 justify='left')
            self.labels_from_list.grid(row=0, rowspan=3, column=0, padx=2, pady=2)
            self.labels_from_list.configure(state='normal')

            self.remove_box = ctk.CTkCheckBox(self.item_label,
                                              text="",
                                              onvalue=1, offvalue=0, variable=on_or_off,
                                              command=partial(self.add_to_removal, items_in_order[4], on_or_off))
            self.remove_box.grid(row=1, column=1, padx=3, pady=3, sticky='nsew')

        self.remove_button = ctk.CTkButton(self,
                                           width=320,
                                           font=self._return_font,
                                           text="Remove",
                                           command=partial(self.removal)
                                           )
        self.remove_button.pack(padx=10, pady=12)
        self.grab_set()
    # ---------------------------------------------------------------------------------------------------------------- #
    # functions to handel the removeal proccess from this instance
    # ---------------------------------------------------------------------------------------------------------------- #

    def add_to_removal(self, items_in_order_pass, on_off):
        if on_off.get() == 1:
            _return_list.append(items_in_order_pass)
        else:
            _return_list.remove(items_in_order_pass)

    def removal(self):
        for row_selected in _return_list:
            for row_to_delete in _order_listed:
                if row_selected == row_to_delete[4]:
                    _order_listed.remove(row_to_delete)
                else:
                    pass
        RemoveItems.destroy(self)


class POSApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.start_index = 0
        self.end_index = 6
        self.order_number_int = None
        self._items_discounted_percent = None
        self._all_items_discounted = []
        self.selection = None
        self.select_items = None
        self.sub_frame = None
        self.order_window_items = None
        self._order_font = None
        self.select_item_label = None
        self.title("Silk Server")

        # self.geometry("1500x950")
        self.menu_path = "Menu/Bin.csv"
        # ------------------------------------------------------------------------------------------------------------ #
        # define variables with empty values
        # ------------------------------------------------------------------------------------------------------------ #
        self._user_info = ['name', 'userid', 'active']
        self.credit_order = 0
        self._button_counter = 0
        self._ticket_listed = []
        global _order_listed
        global _discounted_items_listed
        self._frame_list = []
        self.check_box_values = []
        self.string_text = None
        self.add_total = float(0.00)
        self.total_price = None
        self.price_of_item = None
        self.name_of_item = None
        self.send_log = None
        self.check_box_list = []
        self.master_list_file = "Master_List.csv"
        self._discount_order_amount = 0
        self.from_log = data_mg.GUIObjectList()
        global date_time
        # ------------------------------------------------------------------------------------------------------------ #
        # define theme variables
        # ------------------------------------------------------------------------------------------------------------ #
        global _text
        ctk.set_appearance_mode("dark")
        self._big_font = ctk.CTkFont(family="Helvetica", size=24, weight="bold")
        self._med_font = ctk.CTkFont(family="Helvetica", size=20)
        self._reg_font = ctk.CTkFont(family="Helvetica", size=16)
        self._total_font = ctk.CTkFont(family="Helvetica", size=14, weight="bold")
        # -------------------------------------------------------------------------------------------------------------#
        # main window
        # -------------------------------------------------------------------------------------------------------------#

        self.order_window = ctk.CTkFrame(self)
        self.order_window.grid(row=0, column=0, st='nsew')

        # -------------------------------------------------------------------------------------------------------------#
        # shadow Frames, to hold all objects within context to the main frame
        # -------------------------------------------------------------------------------------------------------------#
        #shadow Frame

        #Frame for total display
        window_total_shadow = ctk.CTkFrame(self.order_window)
        window_total_shadow.grid(row=0, column=0, rowspan=3, padx=10, pady=10)

        #Frame for user window
        #self.user_window = ctk.CTkFrame(self.order_window)
        #self.user_window.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        #Frame for menu items
        self.menu_tab_section = ctk.CTkFrame(self.order_window)
        self.menu_tab_section.grid(row=0, column=1, rowspan=1, padx=10, pady=10, sticky='nsew')
        #Frame for order functions
        order_function_shadow = ctk.CTkFrame(self.order_window)
        order_function_shadow.grid(row=2, column=1, padx=10, pady=10, sticky='nsew')

        # -------------------------------------------------------------------------------------------------------------#
        # orders for current ticket
        # -------------------------------------------------------------------------------------------------------------#

        self.order_number_handler()
        up_button_frame = ctk.CTkFrame(window_total_shadow, width=500)
        up_button_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10, st='nsew')
        up_button = ctk.CTkButton(up_button_frame, text="Up", font=self._reg_font, command=partial(self.scroll_up))
        up_button.pack()


        self.current_order = ctk.CTkFrame(window_total_shadow)
        self.current_order.grid(row=1, column=0, columnspan=3, rowspan=4, padx=12, pady=12, sticky='nsew')
        # StringVar for values in labels

        self.var1_label = ctk.StringVar()
        self.var1_total = ctk.StringVar()
        self.var1_discounts = ctk.StringVar()
        self.var1_tax = ctk.StringVar()
        self.var2_label = ctk.StringVar()
        self.var2_total = ctk.StringVar()
        self.var2_discounts = ctk.StringVar()
        self.var2_tax = ctk.StringVar()
        self.var3_label = ctk.StringVar()
        self.var3_total = ctk.StringVar()
        self.var3_discounts = ctk.StringVar()
        self.var3_tax = ctk.StringVar()
        self.var4_label = ctk.StringVar()
        self.var4_total = ctk.StringVar()
        self.var4_discounts = ctk.StringVar()
        self.var4_tax = ctk.StringVar()
        self.var5_label = ctk.StringVar()
        self.var5_total = ctk.StringVar()
        self.var5_discounts = ctk.StringVar()
        self.var5_tax = ctk.StringVar()
        self.var6_label = ctk.StringVar()
        self.var6_total = ctk.StringVar()
        self.var6_discounts = ctk.StringVar()
        self.var6_tax = ctk.StringVar()
        self.var7_label = ctk.StringVar()
        self.var7_total = ctk.StringVar()
        self.var7_discounts = ctk.StringVar()
        self.var7_tax = ctk.StringVar()

        #Dispaly frames for items
        item_frame1 = ctk.CTkFrame(self.current_order, width=480, height=150)
        item_frame1.grid(row=0, column=0, columnspan=2, padx=7, pady=7, sticky='nsew')

        item1_label = ctk.CTkLabel(item_frame1, width=480,
                                   font=self._total_font,
                                   textvariable=self.var1_label
                                   )
        item1_label.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky='nsew')
        item1_total = ctk.CTkLabel(item_frame1, width=120, font=self._total_font,
                                   textvariable=self.var1_total)
        item1_total.grid(row=1, column=0, padx=10, pady=5, sticky='nsew')
        item1_discounts = ctk.CTkLabel(item_frame1, width=120, font=self._total_font,
                                   textvariable=self.var1_discounts)
        item1_discounts.grid(row=1, column=1, padx=10, pady=5, sticky='nsew')
        item1_tax = ctk.CTkLabel(item_frame1, width=120, font=self._total_font,
                                   textvariable=self.var1_tax)
        item1_tax.grid(row=1, column=2, padx=10, pady=5, sticky='nsew')

        item_frame2 = ctk.CTkFrame(self.current_order, width=480, height=150)
        item_frame2.grid(row=1, column=0, columnspan=2, padx=7, pady=7, sticky='nsew')

        item2_label = ctk.CTkLabel(item_frame2, width=480,
                                   textvariable=self.var2_label, font=self._total_font)
        item2_label.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky='nsew')
        item2_total = ctk.CTkLabel(item_frame2, width=120, font=self._total_font,
                                   textvariable=self.var2_total)
        item2_total.grid(row=1, column=0, padx=10, pady=5, sticky='nsew')
        item2_discounts = ctk.CTkLabel(item_frame2, width=120, font=self._total_font,
                                   textvariable=self.var2_discounts)
        item2_discounts.grid(row=1, column=1, padx=10, pady=5, sticky='nsew')
        item2_tax = ctk.CTkLabel(item_frame2, width=120, font=self._total_font,
                                   textvariable=self.var2_tax)
        item2_tax.grid(row=1, column=2, padx=10, pady=5, sticky='nsew')

        item_frame3 = ctk.CTkFrame(self.current_order, width=480, height=150)
        item_frame3.grid(row=2, column=0, columnspan=2, padx=7, pady=7, sticky='nsew')

        item3_label = ctk.CTkLabel(item_frame3, width=480,
                                   textvariable=self.var3_label,
                                   font=self._total_font)
        item3_label.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky='nsew')
        item3_total = ctk.CTkLabel(item_frame3, width=120, font=self._total_font,
                                   textvariable=self.var3_total)
        item3_total.grid(row=1, column=0, padx=10, pady=5, sticky='nsew')
        item3_discounts = ctk.CTkLabel(item_frame3 ,width=120, font=self._total_font,
                                   textvariable=self.var3_discounts)
        item3_discounts.grid(row=1, column=1, padx=10, pady=5, sticky='nsew')
        item3_tax = ctk.CTkLabel(item_frame3, width=120, font=self._total_font,
                                   textvariable=self.var3_tax)
        item3_tax.grid(row=1, column=2, padx=10, pady=5, sticky='nsew')

        item_frame4 = ctk.CTkFrame(self.current_order, width=480, height=150)
        item_frame4.grid(row=3, column=0, columnspan=2, padx=7, pady=7, sticky='nsew')

        item4_label = ctk.CTkLabel(item_frame4, width=480,
                                   textvariable=self.var4_label,
                                   font=self._total_font)
        item4_label.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky='nsew')
        item4_total = ctk.CTkLabel(item_frame4, width=120,   font=self._total_font,
                                   textvariable=self.var4_total)
        item4_total.grid(row=1, column=0, padx=10, pady=5, sticky='nsew')
        item4_discounts = ctk.CTkLabel(item_frame4, width=120, font=self._total_font,
                                   textvariable=self.var4_discounts)
        item4_discounts.grid(row=1, column=1, padx=10, pady=5, sticky='nsew')
        item4_tax = ctk.CTkLabel(item_frame4, width=120, font=self._total_font,
                                   textvariable=self.var4_tax)
        item4_tax.grid(row=1, column=2, padx=10, pady=5, sticky='nsew')

        item_frame5 = ctk.CTkFrame(self.current_order, width=480, height=150)
        item_frame5.grid(row=4, column=0, columnspan=2, padx=7, pady=7, sticky='nsew')

        item5_label = ctk.CTkLabel(item_frame5, width=480,
                                   textvariable=self.var5_label,
                                   font=self._total_font)
        item5_label.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky='nsew')
        item5_total = ctk.CTkLabel(item_frame5, width=120, font=self._total_font,
                                   textvariable=self.var5_total)
        item5_total.grid(row=1, column=0, padx=10, pady=5, sticky='nsew')
        item5_discounts = ctk.CTkLabel(item_frame5, width=120, font=self._total_font,
                                   textvariable=self.var5_discounts)
        item5_discounts.grid(row=1, column=1, padx=10, pady=5, sticky='nsew')
        item5_tax = ctk.CTkLabel(item_frame5, width=120, font=self._total_font,
                                   textvariable=self.var5_tax)
        item5_tax.grid(row=1, column=2, padx=10, pady=5, sticky='nsew')

        item_frame6 = ctk.CTkFrame(self.current_order, width=480, height=150)
        item_frame6.grid(row=5, column=0, columnspan=2, padx=7, pady=7, sticky='nsew')

        item6_label = ctk.CTkLabel(item_frame6, width=480,
                                   textvariable=self.var6_label,
                                   font=self._total_font)
        item6_label.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky='nsew')
        item6_total = ctk.CTkLabel(item_frame6, width=120, font=self._total_font,
                                   textvariable=self.var6_total)
        item6_total.grid(row=1, column=0, padx=10, pady=5, sticky='nsew')
        item6_discounts = ctk.CTkLabel(item_frame6, width=120, font=self._total_font,
                                   textvariable=self.var6_discounts)
        item6_discounts.grid(row=1, column=1, padx=10, pady=5, sticky='nsew')
        item6_tax = ctk.CTkLabel(item_frame6, width=120, font=self._total_font,
                                   textvariable=self.var6_tax)
        item6_tax.grid(row=1, column=2, padx=10, pady=5, sticky='nsew')

        item_frame7 = ctk.CTkFrame(self.current_order, width=480, height=150)
        item_frame7.grid(row=6, column=0, columnspan=2, padx=7, pady=7, sticky='nsew')

        item7_label = ctk.CTkLabel(item_frame7, width=480,
                                   textvariable=self.var7_label,
                                   font=self._total_font)
        item7_label.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky='nsew')
        item7_total = ctk.CTkLabel(item_frame7, width=120, font=self._total_font,
                                   textvariable=self.var7_total)
        item7_total.grid(row=1, column=0, padx=10, pady=5, sticky='nsew')
        item7_discounts = ctk.CTkLabel(item_frame7, width=120, font=self._total_font,
                                   textvariable=self.var7_discounts)
        item7_discounts.grid(row=1, column=1, padx=10, pady=5, sticky='nsew')
        item7_tax = ctk.CTkLabel(item_frame7, width=120, font=self._total_font,
                                   textvariable=self.var7_tax)
        item7_tax.grid(row=1, column=2, padx=10, pady=5, sticky='nsew')
        # entry boxes
        entry1_label = ctk.CTkEntry(item_frame1, width=480,
                                   textvariable=self.var1_label, font=self._total_font)
        entry1_label.grid()
        entry1_label.grid_forget()
        entry1_total = ctk.CTkEntry(item_frame1, font=self._total_font,
                                   textvariable=self.var1_total)
        entry1_total.grid()
        entry1_total.grid_forget()
        entry1_discounts = ctk.CTkEntry(item_frame1, font=self._reg_font,
                                   textvariable=self.var1_discounts)
        entry1_discounts.grid()
        entry1_discounts.grid_forget()
        entry1_tax = ctk.CTkEntry(item_frame1, font=self._reg_font,
                                   textvariable=self.var1_tax)
        entry1_tax.grid()
        entry1_tax.grid_forget()


        entry2_label = ctk.CTkEntry(item_frame2,
                                   textvariable=self.var2_label)
        entry2_label.grid()
        entry2_label.grid_forget()
        entry2_total = ctk.CTkEntry(item_frame2,
                                   textvariable=self.var2_total)
        entry2_total.grid()
        entry2_total.grid_forget()
        entry2_discounts = ctk.CTkEntry(item_frame2,
                                   textvariable=self.var2_discounts)
        entry2_discounts.grid()
        entry2_discounts.grid_forget()
        entry2_tax = ctk.CTkEntry(item_frame2,
                                   textvariable=self.var2_tax)
        entry2_tax.grid()
        entry2_tax.grid_forget()


        entry3_label = ctk.CTkEntry(item_frame3,
                                   textvariable=self.var3_label)
        entry3_label.grid()
        entry3_label.grid_forget()
        entry3_total = ctk.CTkEntry(item_frame3,
                                   textvariable=self.var3_total)
        entry3_total.grid()
        entry3_total.grid_forget()
        entry3_discounts = ctk.CTkEntry(item_frame3,
                                   textvariable=self.var3_discounts)
        entry3_discounts.grid()
        entry3_discounts.grid_forget()
        entry3_tax = ctk.CTkEntry(item_frame3,
                                   textvariable=self.var3_tax)
        entry3_tax.grid()
        entry3_tax.grid_forget()


        entry4_label = ctk.CTkEntry(item_frame4,
                                   textvariable=self.var4_label)
        entry4_label.grid()
        entry4_label.grid_forget()
        entry4_total = ctk.CTkEntry(item_frame4,
                                   textvariable=self.var4_total)
        entry4_total.grid()
        entry4_total.grid_forget()
        entry4_discounts = ctk.CTkEntry(item_frame4,
                                   textvariable=self.var4_discounts)
        entry4_discounts.grid()
        entry4_discounts.grid_forget()

        entry4_tax = ctk.CTkEntry(item_frame4,
                                   textvariable=self.var4_tax)
        entry4_tax.grid()
        entry4_tax.grid_forget()


        entry5_label = ctk.CTkEntry(item_frame5,
                                   textvariable=self.var5_label)
        entry5_label.grid()
        entry5_label.grid_forget()
        entry5_total = ctk.CTkEntry(item_frame5,
                                   textvariable=self.var5_total)
        entry5_total.grid()
        entry5_total.grid_forget()
        entry5_discounts = ctk.CTkEntry(item_frame5,
                                   textvariable=self.var5_discounts)
        entry5_discounts.grid()
        entry5_discounts.grid_forget()
        entry5_tax = ctk.CTkEntry(item_frame5,
                                   textvariable=self.var5_tax)
        entry5_tax.grid()
        entry5_tax.grid_forget()


        entry6_label = ctk.CTkEntry(item_frame6,
                                   textvariable=self.var6_label)
        entry6_label.grid()
        entry6_label.grid_forget()
        entry6_total = ctk.CTkEntry(item_frame6,
                                   textvariable=self.var6_total)
        entry6_total.grid()
        entry6_total.grid_forget()
        entry6_discounts = ctk.CTkEntry(item_frame6,
                                   textvariable=self.var6_discounts)
        entry6_discounts.grid()
        entry6_discounts.grid_forget()
        entry6_tax = ctk.CTkEntry(item_frame6,
                                   textvariable=self.var6_tax)
        entry6_tax.grid()
        entry6_tax.grid_forget()

        entry7_label = ctk.CTkEntry(item_frame7,
                                   textvariable=self.var7_label)
        entry7_label.grid()
        entry7_label.grid_forget()
        entry7_total = ctk.CTkEntry(item_frame7,
                                   textvariable=self.var7_total)
        entry7_total.grid()
        entry7_total.grid_forget()
        entry7_discounts = ctk.CTkEntry(item_frame7,
                                        textvariable=self.var7_discounts)
        entry7_discounts.grid()
        entry7_discounts.grid_forget()
        entry7_tax = ctk.CTkEntry(item_frame7,
                                  textvariable=self.var7_tax)
        entry7_tax.grid()
        entry7_tax.grid_forget()



        down_button_frame = ctk.CTkFrame(window_total_shadow)
        down_button_frame.grid(row=5, column=0, columnspan=3, padx=10, pady=10, st='nsew')
        down_button = ctk.CTkButton(down_button_frame, text="Down", font=self._reg_font, command=partial(self.scroll_down))
        down_button.pack()
        # -------------------------------------------------------------------------------------------------------------#
        # Total display
        # -------------------------------------------------------------------------------------------------------------#
        # top bar order info
        self.total_window_var = ctk.StringVar()

        self.top_window_labels = ctk.CTkLabel(window_total_shadow, width=500,
                                               font=self._med_font,
                                              textvariable=self.total_window_var)
        self.top_window_labels.grid(row=6, column=0, columnspan=3, sticky='nsew', padx=10, pady=10)

        self.top_window_entry = ctk.CTkEntry(window_total_shadow,
                                             textvariable=self.total_window_var)
        self.top_window_entry.grid_forget()
        # total
        self.total_display_var = ctk.StringVar()

        total_label = ctk.CTkLabel(window_total_shadow, width=150,
                                         font=self._med_font,
                                        text='Total')
        total_label.grid(row=7, column=0, sticky='nsew', padx=3, pady=3)

        total_display = ctk.CTkLabel(window_total_shadow, width=150,height=50,
                                           font=self._med_font,
                                          textvariable=self.total_display_var)
        total_display.grid(row=8, column=0, sticky='nsew', padx=3, pady=3)

        total_display_entry = ctk.CTkEntry(window_total_shadow, textvariable=self.total_display_var)
        total_display_entry.grid_forget()

        # tax
        self.tax_display_var = ctk.StringVar()

        tax_label = ctk.CTkLabel(window_total_shadow, width=150,
                                       font=self._med_font,
                                      text='Tax')
        tax_label.grid(row=7, column=1, sticky='nsew', padx=3, pady=3)

        tax_display = ctk.CTkLabel(window_total_shadow, width=150, height=100,
                                         font=self._med_font,
                                        textvariable=self.tax_display_var)
        tax_display.grid(row=8, column=1, sticky='nsew', padx=3, pady=3)

        tax_display_entry = ctk.CTkEntry(window_total_shadow, textvariable=self.tax_display_var)
        tax_display_entry.grid_forget()

        # subtotal
        self.subtotal_display_var = ctk.StringVar()

        subtotal_label = ctk.CTkLabel(window_total_shadow, width=150,
                                            font=self._med_font,
                                           text='Sub-Total')
        subtotal_label.grid(row=7, column=2, sticky='nsew', padx=3, pady=3)

        subtotal_display = ctk.CTkLabel(window_total_shadow, width=150, height=100,
                                              font=self._med_font,
                                             textvariable=self.subtotal_display_var)
        subtotal_display.grid(row=8, column=2, sticky='nsew', padx=3, pady=3)

        subtotal_display_entry = ctk.CTkEntry(window_total_shadow,
                                                   textvariable=self.subtotal_display_var)
        subtotal_display_entry.grid_forget()
        #--------------------------------------------------------------------------------------------------------------#

        order = ctk.CTkButton(order_function_shadow,
                                   height=50,
                                   text="Order", font=self._reg_font,
                                   command=partial(self.place_order)
                                   )
        order.grid(row=0, column=0, padx=7.5, pady=7.5, sticky='nsew')

        remove = ctk.CTkButton(order_function_shadow,
                                    height=50, 
                                    text="Remove Item", font=self._reg_font,
                                    command=partial(self.remover_handler)
                                    )
        remove.grid(row=0, column=1, padx=7.5, pady=7.5, sticky='nsew')

        discount = ctk.CTkButton(order_function_shadow,
                                      height=50, 
                                      text="Apply Discount", font=self._reg_font,
                                      command=partial(self.apply_discount_handler)
                                      )
        discount.grid(row=1, column=0, padx=7.5, pady=7.5, sticky='nsew')

        credit = ctk.CTkButton(order_function_shadow,
                                    height=50, 
                                    text="Apply Credit", font=self._reg_font,
                                    command=partial(self.apply_credit_handler)
                                    )
        credit.grid(row=1, column=1, padx=7.5, pady=7.5, sticky='nsew')

        cancel = ctk.CTkButton(order_function_shadow,
                                    height=50, width=852, 
                                    text="Cancel", font=self._reg_font,
                                    command=partial(self.cancel_order_handler)
                                    )
        cancel.grid(row=2, column=0, columnspan=2, padx=7.5, pady=7.5, sticky='nsew')

        #--------------------------------------------------------------------------------------------------------------#
        # Frame for user options, logout, user status, user task,
        #--------------------------------------------------------------------------------------------------------------#

        """        self.logout_butt = ctk.CTkButton(self.user_window,
                                         text="Logout", font=self._med_font)
        self.logout_butt.grid(column=3, row=0, sticky='nsew', padx=7.5,  pady=7.5)

        self.status_butt = ctk.CTkButton(self.user_window,
                                         text="Status", font=self._med_font)
        self.status_butt.grid(column=4, row=0, sticky='nsew', padx=7.5,  pady=7.5)

        self.task_butt = ctk.CTkButton(self.user_window,
                                       text="Task", font=self._med_font)
        self.task_butt.grid(column=5, row=0, sticky='nsew', padx=7.5,  pady=7.5)

        self.hours_butt = ctk.CTkButton(self.user_window,
                                        text="Hours/Rate", font=self._med_font)
        self.hours_butt.grid(column=6, row=0, sticky='nsew', padx=7.5,  pady=7.5)

        self.message_butt = ctk.CTkButton(self.user_window,
                                          text="Messages", font=self._med_font)
        self.message_butt.grid(column=3, row=1, sticky='nsew', padx=7.5,  pady=7.5)

        self.sales_butt = ctk.CTkButton(self.user_window,
                                        text="Sales", font=self._med_font)
        self.sales_butt.grid(column=4, row=1, sticky='nsew', padx=7.5, pady=7.5)

        self.help_butt = ctk.CTkButton(self.user_window,
                                       text="Help", font=self._med_font)
        self.help_butt.grid(column=5, row=1, sticky='nsew', padx=7.5,  pady=7.5)

        self.guid_butt = ctk.CTkButton(self.user_window,
                                       text="Menu Guide", font=self._med_font, command=partial(self.menu_guide_handler))
        self.guid_butt.grid(column=6, row=1, sticky='nsew', padx=7.5,  pady=7.5)

        self.user_window_label = ctk.CTkLabel(self.user_window, width=200,
                                              font=self._reg_font,
                                              text='\n' + 'User Name:  ' + self._user_info[0] + '\n' + '\n'
                                              + 'User ID:  ' + self._user_info[1] + '\n' + '\n'
                                              + 'User Status:  ' + self._user_info[2] + '\n'
                                              )
        self.user_window_label.grid(row=0, column=7, rowspan=2,  padx=10, pady=10, sticky='nsew')
        self.update_current_order_window()"""
        #--------------------------------------------------------------------------------------------------------------#
        # Menu Tabs
        #--------------------------------------------------------------------------------------------------------------#


        self.menu_tabs = ctk.CTkTabview(self.menu_tab_section)
        self.menu_tabs.grid(row=0, column=0, padx=10, pady=10)
        menu_tabs = self.from_log.tab_category_list()
        for tabs in menu_tabs:
            menu_name = tabs[0]
            menu_id = tabs[1]
            self.menu_tabs.add(menu_name)
            self.menu_tabs.configure(height=380)
            grid_col = 0
            grid_row = 0
            menu_items = self.from_log.item_in_list(menu_id)
            for items in menu_items:
                item_name = items[0]
                item_price = items[1]
                item_number = items[2]
                self.button = ctk.CTkButton(self.menu_tabs.tab(menu_name), width=200,
                                            text=item_name + '\n' + '\n' + item_price,
                                            font=self._reg_font,
                                            command=partial(self.order_handler, item_name, item_price, item_number))
                self.button.grid(column=grid_col, row=grid_row, sticky='nsew', padx=5, pady=2)
                grid_col += 1
                if grid_col <= 3:
                    grid_row = grid_row
                else:
                    grid_row += 1
                    grid_col = 0

    # ---------------------------------------------------------------------------------------------------------------- #
    # using button handlers as a toplevel function to call the other functions
    # ---------------------------------------------------------------------------------------------------------------- #
    def menu_guide_handler(self):
        menu_popup = MenuGuide()
        self.wait_window(menu_popup)


    def order_number_handler(self):
        self.order_number_int = self.from_log.get_order_number()
        self.current_order_number = str(self.order_number_int)

    def order_handler(self, pass_name, pass_price, pass_id):
        self.add_item_to_list(pass_name, pass_price, pass_id)
        self.update_total_display()
        self.update_current_order_window()
        self.scroll_down()

    def remover_handler(self):
        remove_items_window = RemoveItems()
        self.wait_window(remove_items_window)
        _return_list.clear()
        self.update_total_display()
        self.update_current_order_window()

    def cancel_order_handler(self):
        _order_listed.clear()
        self._discount_order_amount = 0
        self.credit_order = 0
        self.update_total_display()
        self.update_current_order_window()
        self.start_index = 0
        self.end_index = 6

    def apply_discount_handler(self):
        apply_discount_window = ApplyDiscount()
        self.wait_window(apply_discount_window)
        self._discount_order_amount = apply_discount_window.discount_amount
        self._items_discounted_percent = apply_discount_window.discount_amount_item
        if self._items_discounted_percent != 0:
            self.items_to_be_discounted(self._items_discounted_percent)
        self.update_total_display()
        self.update_current_order_window()

    def apply_credit_handler(self):
        if self.credit_order == 0:
            apply_credit = ApplyCredit()
            self.wait_window(apply_credit)
            credit_for_order = apply_credit.credit
            self.credit_order = credit_for_order
            if self.credit_order == 0:
                pass
            else:
                self.update_total_display()
                self.update_current_order_window()
        else:
            credit_exception3 = ' No more than one credit per order '
            pop_up = Exceptions(credit_exception3)
            self.wait_window(pop_up)

    def scroll_up(self):
        if self.start_index > 0:
            self.start_index -= 1
            self.end_index -= 1
            self.update_current_order_window()

    def scroll_down(self):
        if self.end_index < len(_order_listed) - 1:
            self.start_index += 1
            self.end_index += 1
            self.update_current_order_window()

    def place_order(self):
        log_total, log_tax, log_sub =\
            sales_calculator.totaler(_order_listed, self._discount_order_amount, self.credit_order)

        l_total = float(log_total)
        l_tax = float(log_tax)
        l_sub = log_sub
        l_discount = int(self._discount_order_amount)
        l_credit = int(self.credit_order)

        order_added = [self.order_number_int, l_total, l_tax, l_sub, date_time, l_discount, l_credit,
                       10001, 1001, 10000001, 0]
        data_mg.log_to_order(order_added)

        for items_data in _order_listed:
            _discount = 0
            _named = items_data[0]
            t_totaled = items_data[1]
            _totaled = float(t_totaled)
            t_taxed = items_data[2]
            _taxed = float(t_taxed)
            t_code = items_data[3]
            _code = int(t_code)
            t_counter = items_data[4]
            _counter = int(t_counter)
            for discount in self._all_items_discounted:
                discount_int = discount[0]
                if _code in discount:
                    _discount = discount_int
                else:
                    _discount = 0
            items_added = [_code, self.order_number_int, _named, _totaled, _taxed, _discount]
            # Item_ID INTEGER, Order_ID INTEGER, _name TEXT, _price REAL, _tax REAL, _discount INTEGER
            data_mg.log_to_item_orders(items_added)

        self.order_number_handler()
        self.cancel_order_handler()
        self.start_index = 0
        self.end_index = 6

    def refresher(self):
        self.update()

    # ---------------------------------------------------------------------------------------------------------------- #
    # functions to handel list
    # ---------------------------------------------------------------------------------------------------------------- #

    def add_item_to_list(self, button_named, button_total, item_code):
        self._button_counter += 1
        totaled_float = float(button_total[1:])
        button_taxed = sales_calculator.taxer(totaled_float)
        button_taxed = '{:.2f}'.format(button_taxed)
        button_totaled = '{:.2f}'.format(totaled_float)
        _order_listed.append([button_named, button_totaled, button_taxed, item_code, self._button_counter])

    def items_to_be_discounted(self, percentage_for_items):
        for items_cost_before in _order_listed:
            for items_selected in _discounted_items_listed:
                if items_selected == items_cost_before[4]:
                    items_cost_passer = items_cost_before[1]
                    item_discounted_cost, tax_discounted = sales_calculator.discount_item(items_cost_passer,
                                                                                          percentage_for_items)
                    items_cost_before[2] = tax_discounted
                    items_cost_before[1] = item_discounted_cost
                    self._all_items_discounted.append([items_selected, percentage_for_items])
        _discounted_items_listed.clear()


    # ---------------------------------------------------------------------------------------------------------------- #
    # functions to handel the display
    # ---------------------------------------------------------------------------------------------------------------- #

    def update_total_display(self):
        display_total, display_tax, display_sub = \
            sales_calculator.totaler(_order_listed, self._discount_order_amount, self.credit_order)
        display_count = len(_order_listed)
        display_total_str = '{:.2f}'.format(display_total)
        display_tax_str = '{:.2f}'.format(display_tax)
        display_sub_str = '{:.2f}'.format(display_sub)
        display_count_str = display_count
        display_total_str = str(display_total_str)
        display_tax_str = str(display_tax_str)
        display_sub_str = str(display_sub_str)
        display_count_str = str(display_count_str)
        label_for_window = 'Order Number: ' + self.current_order_number + ' Number of items: ' + display_count_str
        self.total_display_var.set(display_total_str)
        self.tax_display_var.set(display_tax_str)
        self.subtotal_display_var.set(display_sub_str)
        self.total_window_var.set(label_for_window)

    def update_current_order_window(self):
        item_data7, item_data6, item_data5, item_data4, item_data3, item_data2, item_data1 = self.item_shown_by_number()
        butt_count1 = str(item_data1[4])
        sku_item1 = str(item_data1[3])
        item_named1 = str(item_data1[0])
        item_data_string = ('Item #' + butt_count1 + '   ID:  ' + sku_item1 + '    Item: ' + item_named1)
        self.var1_label.set(str(item_data_string))
        str_var1_total = ('Total: $'+ str(item_data1[1]))
        self.var1_total.set(str_var1_total)
        str_var1_discounts = ' Discounts: % '
        self.var1_discounts.set(str_var1_discounts)
        str_var1_tax = ('tax: $' + str(item_data1[2]))
        self.var1_tax.set(str_var1_tax)

        butt_count2 = str(item_data2[4])
        sku_item2 = str(item_data2[3])
        item_named2 = str(item_data2[0])
        item2_data_string = ('Item #  ' + butt_count2 + '   ID:  ' + sku_item2 + '    Item: ' + item_named2)
        self.var2_label.set(str(item2_data_string))
        str_var2_total = ('Total: $' + str(item_data2[1]))
        self.var2_total.set(str_var2_total)
        str_var2_discounts = ('Discounts: %' + str(item_data2[2]))
        self.var2_discounts.set(str_var2_discounts)
        str_var2_tax = ('Tax: $' + str(item_data2[2]))
        self.var2_tax.set(str_var2_tax)

        butt_count3 = str(item_data3[4])
        sku_item3 = str(item_data3[3])
        item_named3 = str(item_data3[0])
        item_data_string = ('Item #' + butt_count3 + '   ID:  ' + sku_item3 + '    Item: ' + item_named3)
        self.var3_label.set(str(item_data_string))
        str_var3_total = ('Total: $' + str(item_data3[1]))
        self.var3_total.set(str_var3_total)
        str_var3_discounts = 'Discounts: %'
        self.var3_discounts.set(str_var3_discounts)
        str_var3_tax = ('Tax: $' + str(item_data3[2]))
        self.var3_tax.set(str(str_var3_tax))

        butt_count4 = str(item_data4[4])
        sku_item4 = str(item_data4[3])
        item_named4 = str(item_data4[0])
        item4_data_string = ('Item #' + butt_count4 + '   ID:  ' + sku_item4 + '    Item: ' + item_named4)
        self.var4_label.set(str(item4_data_string))
        str_var4_total = ('Total: $' + str(item_data4[1]))
        self.var4_total.set(str_var4_total)
        str_var4_discounts = 'Discounts: %'
        self.var4_discounts.set(str_var4_discounts)
        str_var4_tax = ('Tax: $' + str(item_data4[2]))
        self.var4_tax.set(str_var4_tax)

        butt_count5 = str(item_data5[4])
        sku_item5 = str(item_data5[3])
        item_named5 = str(item_data5[0])
        item_data_string = ('Item #' + butt_count5 + '   ID:  ' + sku_item5 + '    Item: ' + item_named5 )
        self.var5_label.set(str(item_data_string))
        str_var5_total = ('Total: $' + str(item_data5[1]))
        self.var5_total.set(str_var5_total)
        str_var5_discounts = 'Discounts: %'
        self.var5_discounts.set(str_var5_discounts)
        str_var5_tax = ('Tax: $' + str(item_data5[2]))
        self.var5_tax.set(str_var5_tax)

        butt_count6 = str(item_data6[4])
        sku_item6 = str(item_data6[3])
        item_named6 = str(item_data6[0])
        item6_data_string = ('Item #' + butt_count6  + '   ID:  ' + sku_item6 + '    Item: ' + item_named6)
        self.var6_label.set(str(item6_data_string))
        str_var6_total = ('Total: $' + str(item_data6[1]))
        self.var6_total.set(str_var6_total)
        str_var6_discounts = 'Discounts: %'
        self.var6_discounts.set(str_var6_discounts)
        str_var6_tax = ('Tax: $' + str(item_data6[2]))
        self.var6_tax.set(str_var6_tax)

        butt_count7 = str(item_data7[4])
        sku_item7 = str(item_data7[3])
        item_named7 = str(item_data7[0])
        item7_data_string = ('Item #' + butt_count7 + '   ID:  ' + sku_item7 + '    Item: ' + item_named7 )
        self.var7_label.set(str(item7_data_string))
        str_var7_total = ('Total: $' + str(item_data7[1]))
        self.var7_total.set(str_var7_total)
        str_var7_discounts = 'Discounts: %'
        self.var7_discounts.set(str_var7_discounts)
        str_var7_tax = ('Tax: $' + str(item_data7[2]))
        self.var7_tax.set(str_var7_tax)



    def item_shown_by_number(self):
        place_holder_item = [0, 0, 0, 0, 0]
        item_data = []

        if not _order_listed:
            item_data = [place_holder_item] * 7
        else:
            start_index = self.start_index
            end_index = self.end_index
            last_index = len(_order_listed) - 1

            for item_index in range(start_index, end_index + 1):
                if last_index >= item_index:
                    item_data.append(_order_listed[item_index])
                elif last_index < item_index:
                    item_data.append(place_holder_item)

        return tuple(item_data[::-1])


    # --------------------------------------------------------------------------------------------------------------#
#functions for current_orders
# --------------------------------------------------------------------------------------------------------------#





if __name__ == "__main__":
    data_mg.initialization_process()
    root = POSApp()


    root.mainloop()


