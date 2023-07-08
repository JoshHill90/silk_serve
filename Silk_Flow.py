import customtkinter as ctk
import tkinter as tk
import data_manager as data_mg
from functools import partial
import datetime
from tkcalendar import *

# ---------------------------------------------------------------------------------------------------------------- #
# color and them variables
# ---------------------------------------------------------------------------------------------------------------- #
_color_main = "#007373"
_color_light = "#009999"
_color_dark = "#003939"
_color_med = "#001313"
_color_gray = "#708383"
_color_white = "#DFF2F2"
_color_shadow = "#0c1717"
_text = "black"

# ---------------------------------------------------------------------------------------------------------------- #
# global list
# ---------------------------------------------------------------------------------------------------------------- #
date_and_time = datetime.datetime.now()
dates = date_and_time.date()
times = date_and_time.strftime("%I:%M:%S %p")
date = str(dates)
time = str(times)
date_time = 'DATE | ' + date + ' TIME | ' + time

get_from = data_mg.GUIObjectList()
orders, items_in_orders = get_from.logged_tickets()
ctk.set_default_color_theme('Themes/delta4.txt')

def todays_date():
    date_of_orders = str(date_time)
    this_year_str = str(date_of_orders[9:11])
    get_month = int(date_of_orders[12:14])
    this_month_str = str(get_month)
    get_day = int(date_of_orders[15:17])
    this_day_str = str(get_day)
    date_check = this_month_str + '/' + this_day_str + '/' + this_year_str
    return date_check

class DateSelector(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        frame_for_cal = ctk.CTkFrame(self, )
        frame_for_cal.pack(padx=20, pady=20)

        self.cal = Calendar(self, selectmode='day',
                            year=2020, month=5,
                            day=22)

        self.cal.pack(pady=20)
        _date = todays_date()
        Calendar.selection_set(self.cal, _date)
        cal_button = ctk.CTkButton(frame_for_cal, text="Get Date",
                                   command=lambda: self.get_selected_date())
        cal_button.pack(padx=10, pady=10)
        self.send_date = None
        self.grab_set()



    def get_selected_date(self):
        self.send_date = self.cal.get_date()
        print('get date', self.send_date)
        self.destroy()



class SilkFlow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.date_val = ctk.StringVar()
        self.number_val = ctk.StringVar()
        self.date_box = None
        self.from_calendar = None
        self.search_scope = None
        self.search_this_date = None
        self.search_box = None
        self.current_view = None
        self.ticket_log_button = None
        self.data_structure_frame = None
        self.employee_button = None
        self.stats_button = None
        self.vendors_button = None
        self.hours_button = None
        self.returns_button = None
        self.sales_button = None
        self.inventory_button = None
        self.data_view = None
        self.inventory_frame = None
        self.filtered_orders = None
        global orders
        global items_in_orders
        global _color_main
        global _color_light
        global _color_dark
        global _color_med
        global _color_gray
        global _color_white
        global _color_shadow
        global _text
        ctk.set_appearance_mode("dark")
        self._big_font = ctk.CTkFont(family="Helvetica", size=24, weight="bold")
        self._med_font = ctk.CTkFont(family="Helvetica", size=20)
        self._reg_font = ctk.CTkFont(family="Helvetica", size=16)
        self._total_font = ctk.CTkFont(family="Helvetica", size=34, weight="bold")

        self.inventory_frame = ctk.CTkFrame(self, )
        self.inventory_frame.pack(padx=10, pady=10)

        self.section1_frame = ctk.CTkFrame(self.inventory_frame,  width=350)
        self.section1_frame.grid(row=0, column=0, rowspan=3, padx=10, pady=10, sticky='nsew')

        self.section2_frame = ctk.CTkFrame(self.inventory_frame,  height=125)
        self.section2_frame.grid(row=0, column=1, columnspan=4, padx=10, pady=10, sticky='nsew')

        self.window_view = ctk.CTkScrollableFrame(self.inventory_frame,  width=1070, height=750)
        self.window_view.grid(row=1, column=1, rowspan=4, columnspan=4, padx=10, pady=10, sticky='nsew')
    #emp1

    def main_menu(self):
        print('emp1')
        self.data_structure_frame = ctk.CTkFrame(self.section1_frame,  width=315)
        self.data_structure_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.data_view = ctk.CTkLabel(self.data_structure_frame,
                                      
                                      width=180,
                                      height=120,
                                      font=self._big_font,
                                      text_color=_color_white,
                                      text='Data Structures'
                                      )
        self.data_view.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        self.inventory_button = ctk.CTkButton(self.data_structure_frame,
                                              
                                              width=180,
                                              height=65,
                                              text_color=_color_white,
                                              text='Inventory',
                                              font=self._med_font)
        self.inventory_button.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        self.sales_button = ctk.CTkButton(self.data_structure_frame,
                                          
                                          width=180,
                                          height=65,
                                          text_color=_color_white,
                                          text='Sales',
                                          font=self._med_font,
                                          command=partial(self.sales_view_handler)
                                          )
        self.sales_button.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')

        self.hours_button = ctk.CTkButton(self.data_structure_frame,
                                          width=180,
                                          height=65,
                                          text_color=_color_white,
                                          text='Hours',
                                          font=self._med_font)
        self.hours_button.grid(row=4, column=0, padx=10, pady=10, sticky='nsew')
        self.stats_button = ctk.CTkButton(self.data_structure_frame,
                                          
                                          width=180,
                                          height=65,
                                          text_color=_color_white,
                                          text='Stats',
                                          font=self._med_font)
        self.stats_button.grid(row=5, column=0, padx=10, pady=10, sticky='nsew')

        self.vendors_button = ctk.CTkButton(self.data_structure_frame,
                                            
                                            width=180,
                                            height=65,
                                            text_color=_color_white,
                                            text='Vendors',
                                            font=self._med_font)
        self.vendors_button.grid(row=6, column=0, padx=10, pady=10, sticky='nsew')

        self.employee_button = ctk.CTkButton(self.data_structure_frame,
                                             
                                             width=180,
                                             height=65,
                                             text_color=_color_white,
                                             text='Employees',
                                             font=self._med_font)
        self.employee_button.grid(row=7, column=0, padx=10, pady=10, sticky='nsew')

    #emp11

    def main_menu_refresh(self):
        print('emp11')
        self.window_view.destroy()
        self.data_structure_frame.destroy()
        self.main_menu()

    # ---------------------------------------------------------------------------------------------------------------- #
    # sales data menu
    # ---------------------------------------------------------------------------------------------------------------- #

    #emp2

    def sales_data(self):
        print('emp2')
        self.data_structure_frame = ctk.CTkFrame(self.section1_frame,  width=315)
        self.data_structure_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.data_view = ctk.CTkLabel(self.data_structure_frame,
                                      
                                      width=180,
                                      height=120,
                                      font=self._big_font,
                                      text_color=_color_white,
                                      text='Sales Data'
                                      )
        self.data_view.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        self.ticket_log_button = ctk.CTkButton(self.data_structure_frame,
                                               
                                               width=180,
                                               height=65,
                                               text_color=_color_white,
                                               text='Ticket Log',
                                               font=self._med_font)
        self.ticket_log_button.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
        self.ticket_log_button = ctk.CTkButton(self.data_structure_frame,
                                               
                                               width=180,
                                               height=65,
                                               text_color=_color_white,
                                               text='Data Structures',
                                               font=self._med_font,
                                               command=partial(self.main_menu_refresh))
        self.ticket_log_button.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')

    #emp3

    def ticket_log_view(self, _ticket_list):
        print('emp3')
        self.window_view = ctk.CTkScrollableFrame(self.inventory_frame,  width=1070, height=750)
        self.window_view.grid(row=1, column=1, rowspan=4, columnspan=4, padx=10, pady=10, sticky='nsew')
        self.current_view = ctk.CTkFrame(self.window_view,  width=315)
        self.current_view.grid(row=0, column=0, padx=5, pady=5)
        self.data_view = ctk.CTkLabel(self.current_view,
                                      
                                      width=180,
                                      height=120,
                                      font=self._big_font,
                                      text_color=_color_white,
                                      text='Tickets'
                                      )
        self.data_view.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')

        ticket_num = 1
        for order in _ticket_list:
            call_id = order[1]
            to_id = str(order[0])
            to_number = str(order[1])
            from_total = "{:.2f}".format(order[2])
            to_total = str(from_total)
            from_tax = "{:.2f}".format(order[3])
            to_tax = str(from_tax)
            from_sub_total = "{:.2f}".format(order[4])
            to_sub_total = str(from_sub_total)
            to_discounts = str(order[6])
            to_credit = str(order[7])

            o_id = '| Order Id \n ' + to_id
            o_number = ' Order Number \n ' + to_number
            o_total = "   Order Total \n " + to_total
            o_tax = '   Order Tax \n ' + to_tax
            o_sub_total = '   Order Sub Total \n ' + to_sub_total
            o_date = order[5]
            o_discounts = 'Discount applied to order\n ' + to_discounts
            o_credit = '  Credit applied to order \n ' + to_credit

            self.order_frame = ctk.CTkFrame(self.current_view,
                                             width=1050,
                                             height=144,
                                             )
            self.order_frame.grid(row=ticket_num, column=0, padx=7, pady=7, sticky='nsew')

            # order details
            self.order_date = ctk.CTkLabel(self.order_frame,
                                              
                                              width=185, height=70,
                                              font=self._reg_font,
                                              text_color=_color_white,
                                              text=o_date
                                              )
            self.order_date.grid(row=0, column=0, columnspan=2, padx=3, pady=3, sticky='nsew')

            self.order_id = ctk.CTkLabel(self.order_frame,
                                              
                                              width=185, height=70,
                                              font=self._reg_font,
                                              text_color=_color_white,
                                              text=o_id,
                                              )
            self.order_id.grid(row=1, column=0, padx=3, pady=3, sticky='nsew')

            self.order_number = ctk.CTkLabel(self.order_frame,
                                              
                                              width=185, height=70,
                                              font=self._reg_font,
                                              text_color=_color_white,
                                              text=o_number
                                              )
            self.order_number.grid(row=1, column=1, padx=3, pady=3, sticky='nsew')

            self.order_total = ctk.CTkLabel(self.order_frame,
                                              
                                              width=185, height=70,
                                              font=self._reg_font,
                                              text_color=_color_white,
                                              text=o_total
                                              )
            self.order_total.grid(row=0, column=2, padx=3, pady=3, sticky='nsew')

            self.order_tax = ctk.CTkLabel(self.order_frame,
                                              
                                              width=185, height=70,
                                              font=self._reg_font,
                                              text_color=_color_white,
                                              text=o_tax
                                              )
            self.order_tax.grid(row=0, column=3, padx=3, pady=3, sticky='nsew')

            self.order_sub_total = ctk.CTkLabel(self.order_frame,
                                              
                                              width=185, height=70,
                                              font=self._reg_font,
                                              text_color=_color_white,
                                              text=o_sub_total
                                              )
            self.order_sub_total.grid(row=0, column=4, padx=3, pady=3, sticky='nsew')

            self.order_discounts = ctk.CTkLabel(self.order_frame,
                                              
                                              width=185, height=70,
                                              font=self._reg_font,
                                              text_color=_color_white,
                                              text=o_discounts
                                              )
            self.order_discounts.grid(row=1, column=2, padx=3, pady=3, sticky='nsew')

            self.order_credit = ctk.CTkLabel(self.order_frame,
                                              
                                              width=185, height=70,
                                              font=self._reg_font,
                                              text_color=_color_white,
                                              text=o_credit
                                              )
            self.order_credit.grid(row=1, column=3, padx=3, pady=3, sticky='nsew')

            self.order_details = ctk.CTkButton(self.order_frame,
                                             
                                             width=185, height=70,
                                             font=self._reg_font,
                                             text_color=_color_white,
                                             text='Ticket Details',
                                             command=partial(self.items_on_ticket, call_id, items_in_orders, order)
                                             )
            self.order_details.grid(row=1, column=4, padx=3, pady=3, sticky='nsew')

            ticket_num += 1

    #emp4

    def filter_and_search(self):
        print('emp4')
        self.section2_frame = ctk.CTkFrame(self.inventory_frame,  height=125)
        self.section2_frame.grid(row=0, column=1, columnspan=4, padx=10, pady=10, sticky='nsew')
        if self.search_scope is None:
            search_option_var = ctk.StringVar(value="Order Number")
            self.search_scope = 'Order Number'
            self.search_box = ctk.CTkEntry(self.section2_frame, placeholder_text='Search by Order Number',
                                           textvariable=self.number_val)
            self.search_box.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
            search_button = ctk.CTkButton(self.section2_frame,  text='Search',
                                          font=self._reg_font,
                                          command=partial(self.sales_filter_refresh, self.search_scope))
            search_button.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
            search_option = ctk.CTkOptionMenu(self.section2_frame, values=["Order Number", "Date"],
                                              command=self.search_callback,
                                              variable=search_option_var)
            search_option.grid(row=0, column=1, padx=10, pady=10)
        elif self.search_scope == 'Date':
            search_option_var = ctk.StringVar(value="Date")
            search_button = ctk.CTkButton(self.section2_frame,  text='Search',
                                          font=self._reg_font,
                                          command=partial(self.sales_filter_refresh, self.search_scope))
            search_button.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
            search_option = ctk.CTkOptionMenu(self.section2_frame, values=["Order Number", "Date"],
                                              command=self.search_callback,
                                              variable=search_option_var)
            search_option.grid(row=0, column=1, padx=10, pady=10)
            date_selector_button = ctk.CTkButton(self.section2_frame, text='Select a Date',
                                                 command=partial(self.select_calendar_date))
            date_selector_button.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')



            self.date_box = ctk.CTkEntry(self.section2_frame,
                                         textvariable=self.date_val)
            self.date_box.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')


        elif self.search_scope == 'Order Number':
            search_option_var = ctk.StringVar(value="Order Number")
            search_option = ctk.CTkOptionMenu(self.section2_frame, values=["Order Number", "Date"],
                                              command=self.search_callback,
                                              variable=search_option_var)
            search_option.grid(row=0, column=1, padx=10, pady=10)

            self.search_box = ctk.CTkEntry(self.section2_frame, placeholder_text='Search by Order Number',
                                           textvariable=self.number_val)
            self.search_box.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
            search_button = ctk.CTkButton(self.section2_frame,  text='Search',
                                          font=self._reg_font,
                                          command=partial(self.sales_filter_refresh, self.search_scope))
            search_button.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

    #emp5

    def select_calendar_date(self):
        print('emp5')
        get_date = DateSelector()
        self.wait_window(get_date)
        search_date = get_date.send_date
        if search_date is None:
            search_date = todays_date()
        else:
            pass

        self.date_val.set(search_date)
        search_ = self.date_box.get()
        print(search_, 'returning')


    #emp6

    def search_functions(self, search_type=None):
        print('emp6')
        if search_type is None:
            all_tickets = orders
            return all_tickets

        elif search_type == 'Date':
            get_filter_date = self.date_box.get()
            print('this get', type(get_filter_date))
            filter_by_date = []
            for dates_selected in orders:
                date_of_orders = dates_selected[5]
                year_in = str(date_of_orders[9:11])
                from_month = int(date_of_orders[12:14])
                month_in = str(from_month)
                from_day = int(date_of_orders[15:17])
                day_in = str(from_day)
                date_check = month_in + '/' + day_in + '/' + year_in
                print(date_check, '$$1', get_filter_date, "$$2")
                if get_filter_date == date_check:
                    filter_by_date.append(dates_selected)
            return filter_by_date

        elif search_type == 'Order Number':
            search = int(self.search_box.get())
            filtered_by_number = []
            for order in orders:
                if order[1] == search:
                    filtered_by_number.append(order)
            return filtered_by_number
        else:
            # Invalid search criteria
            return

    #emp7

    def search_callback(self, choice):
        print('emp7')
        self.search_scope = choice
        self.sales_view_handler()

    #emp8

    def items_on_ticket(self, order_number, items_in_list, order_ticket):
        print('emp8')
        self.window_view.destroy()
        self.window_view = ctk.CTkScrollableFrame(self.inventory_frame,  width=1070, height=750)
        self.window_view.grid(row=1, column=1, rowspan=4, columnspan=4, padx=10, pady=10, sticky='nsew')
        to_id = str(order_ticket[0])
        to_number = str(order_ticket[1])
        from_total = "{:.2f}".format(order_ticket[2])
        to_total = str(from_total)
        from_tax = "{:.2f}".format(order_ticket[3])
        to_tax = str(from_tax)
        from_sub_total = "{:.2f}".format(order_ticket[4])
        to_sub_total = str(from_sub_total)
        to_discounts = str(order_ticket[6])
        to_credit = str(order_ticket[7])

        iit_id = 'Order Id\n' + to_id
        iit_number = 'Order Number\n' + to_number
        iit_total = "Order Total\n" + to_total
        iit_tax = 'Order Tax\n' + to_tax
        iit_sub_total = 'Order Sub Total\n' + to_sub_total
        iit_date = order_ticket[5]
        iit_discounts = 'Discount applied to order\n' + to_discounts
        iit_credit = 'Credit applied to order\n' + to_credit
        self.current_view = ctk.CTkFrame(self.window_view,  width=315)
        self.current_view.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        self.ticket_frame = ctk.CTkFrame(self.current_view,
                                         width=1050,
                                         height=144,
                                         )
        self.ticket_frame.grid(row=0, column=0, padx=7, pady=7, sticky='nsew')

        # order details
        self.item_date = ctk.CTkLabel(self.ticket_frame,
                                      
                                      width=185, height=70,
                                      font=self._reg_font,
                                      text_color=_color_white,
                                      text=iit_date
                                      )
        self.item_date.grid(row=0, column=0, columnspan=2, padx=3, pady=3, sticky='nsew')

        self.item_id = ctk.CTkLabel(self.ticket_frame,
                                    
                                    width=185, height=70,
                                    font=self._reg_font,
                                    text_color=_color_white,
                                    text=iit_id,
                                    )
        self.item_id.grid(row=1, column=0, padx=3, pady=3, sticky='nsew')

        self.item_number = ctk.CTkLabel(self.ticket_frame,
                                        
                                        width=185, height=70,
                                        font=self._reg_font,
                                        text_color=_color_white,
                                        text=iit_number
                                        )
        self.item_number.grid(row=1, column=1, padx=3, pady=3, sticky='nsew')

        self.item_total = ctk.CTkLabel(self.ticket_frame,
                                       
                                       width=185, height=70,
                                       font=self._reg_font,
                                       text_color=_color_white,
                                       text=iit_total
                                       )
        self.item_total.grid(row=0, column=2, padx=3, pady=3, sticky='nsew')

        self.item_tax = ctk.CTkLabel(self.ticket_frame,
                                     
                                     width=185, height=70,
                                     font=self._reg_font,
                                     text_color=_color_white,
                                     text=iit_tax
                                     )
        self.item_tax.grid(row=0, column=3, padx=3, pady=3, sticky='nsew')

        self.item_sub_total = ctk.CTkLabel(self.ticket_frame,
                                           
                                           width=185, height=70,
                                           font=self._reg_font,
                                           text_color=_color_white,
                                           text=iit_sub_total
                                           )
        self.item_sub_total.grid(row=0, column=4, padx=3, pady=3, sticky='nsew')

        self.item_discounts = ctk.CTkLabel(self.ticket_frame,
                                           
                                           width=185, height=70,
                                           font=self._reg_font,
                                           text_color=_color_white,
                                           text=iit_discounts
                                           )
        self.item_discounts.grid(row=1, column=2, padx=3, pady=3, sticky='nsew')

        self.item_credit = ctk.CTkLabel(self.ticket_frame,
                                        
                                        width=185, height=70,
                                        font=self._reg_font,
                                        text_color=_color_white,
                                        text=iit_credit
                                        )
        self.item_credit.grid(row=1, column=3, padx=3, pady=3, sticky='nsew')
        item_number_count = 1
        for items in items_in_list:
            number_check = int(items[2])
            if order_number == number_check:
                str_item_id = str(items[1])
                str_item_name = items[3]
                str_item_cost = str(items[4])
                str_item_tax = str(items[5])
                str_item_discount = str(items[6])
                item_id = 'Item ID \n' + str_item_id
                item_name = 'Item Name \n' + str_item_name
                item_cost = 'Price of Item \n' + str_item_cost
                item_tax = 'Tax Applied \n' + str_item_tax
                item_discount = 'Item Discount\n' + str_item_discount
                #item details
                self.item_frame = ctk.CTkFrame(self.current_view,
                                                 width=1050,
                                                 height=144,
                                                 )
                self.item_frame.grid(row=item_number_count, column=0, padx=7, pady=7, sticky='nsew')

                # order details
                self.iit_id_label = ctk.CTkLabel(self.item_frame,
                                              
                                              width=185, height=70,
                                              font=self._reg_font,
                                              text_color=_color_white,
                                              text=item_id
                                              )
                self.iit_id_label.grid(row=0, column=0, padx=3, pady=3, sticky='nsew')
                self.iit_name_label = ctk.CTkLabel(self.item_frame,
                                              
                                              width=185, height=70,
                                              font=self._reg_font,
                                              text_color=_color_white,
                                              text=item_name
                                              )
                self.iit_name_label.grid(row=0, column=1, padx=3, pady=3, sticky='nsew')
                self.iit_cost_label = ctk.CTkLabel(self.item_frame,
                                              
                                              width=185, height=70,
                                              font=self._reg_font,
                                              text_color=_color_white,
                                              text=item_cost
                                              )
                self.iit_cost_label.grid(row=0, column=2, padx=3, pady=3, sticky='nsew')
                self.iit_tax_label = ctk.CTkLabel(self.item_frame,
                                              
                                              width=185, height=70,
                                              font=self._reg_font,
                                              text_color=_color_white,
                                              text=item_tax
                                              )
                self.iit_tax_label.grid(row=0, column=3, padx=3, pady=3, sticky='nsew')
                self.iit_discount_label = ctk.CTkLabel(self.item_frame,
                                              
                                              width=185, height=70,
                                              font=self._reg_font,
                                              text_color=_color_white,
                                              text=item_discount
                                              )
                self.iit_discount_label.grid(row=0, column=4, padx=3, pady=3, sticky='nsew')
                item_number_count +=1

    #emp9

    def sales_view_handler(self):
        print('emp9')

        self.data_structure_frame.destroy()
        self.sales_data()
        self.section2_frame.destroy()
        self.filter_and_search()
        self.window_view.destroy()
        clear_list = None
        clear_list_pass = self.search_functions(clear_list)
        self.ticket_log_view(clear_list_pass)

    #emp10

    def sales_filter_refresh(self, search_pass):
        print('emp10')

        self.data_structure_frame.destroy()
        self.sales_data()
        self.section2_frame.destroy()
        self.filter_and_search()
        self.window_view.destroy()
        list_pass = self.search_functions(search_pass)
        self.ticket_log_view(list_pass)
















if __name__ == "__main__":
    data_mg.initialization_process()

    root = SilkFlow()
    root.main_menu()



    root.mainloop()

