from tkinter import *
import parser
from tkinter import ttk


def make_started_window(root=None):

    if root is not None:
        root.destroy()

    def button_clicked():
        scraper_window(started_window, url_entry.get())

    started_window = Tk()
    started_window.title("eBay Scraper")
    started_window.geometry("400x250")
    started_window.resizable(False, False)

    title = Label(text="Enter the URL of the Seller page", font=10)
    title.place(x=85, y=80)

    url_entry = Entry(width=30)
    url_entry.place(x=105, y=110)

    button = Button(text="Submit", command=button_clicked)
    button.place(x=160, y=135, width=70, height=40)

    started_window.mainloop()

def scraper_window(root, url):
    pars = parser.Parser(url)
    pars.change_url_to_seller_all_products()
    pars.get_information()

    root.destroy()
    root = Tk()
    root.title("eBay Scraper")
    root.geometry("350x380")
    root.resizable(False, False)

    def get_back():
        make_started_window(root)

    get_back_button = ttk.Button(text="Get back", command=get_back)
    get_back_button.grid(row=0, column=0)

    information_label = Label(text="INFORMATION", font=16)
    information_label.grid(row=0, column=1, pady=10)

    seller = Label(text="Seller: ", font=12)
    seller.grid(row=1, column=0, sticky="w", pady=5)

    seller_name = Label(text=pars.information_dct["Seller"], font=7)
    seller_name.grid(row=1, column=1, sticky="w")

    feedback = Label(text="Feedback: ", font=12)
    feedback.grid(row=2, column=0, sticky="w", pady=5)

    seller_feedback = Label(text=pars.information_dct["Feedback"], font=7)
    seller_feedback.grid(row=2, column=1, sticky="w")

    items_sold = Label(text="Items Sold: ", font=12)
    items_sold.grid(row=3, column=0, sticky="w", pady=5)

    seller_items_sold = Label(text=pars.information_dct["Items Sold"], font=7)
    seller_items_sold.grid(row=3, column=1, sticky="w")

    followers = Label(text="Followers: ", font=12)
    followers.grid(row=4, column=0, sticky="w", pady=5)

    seller_followers = Label(text=pars.information_dct["Followers"], font=7)
    seller_followers.grid(row=4, column=1, sticky="w", pady=5)

    scraper_label = Label(text="SCRAPER", font=16)
    scraper_label.grid(row=5, column=1, pady=10)

    category_label = Label(text="Choose\nCategory: ", font=12)
    category_label.grid(row=6, column=0)

    def category_combobox_selected(event):
        pars.choose_category(category_combobox.get())
        pars.get_items_in_category()
        items_in_category["text"] = pars.information_dct["Items Count"]
        items_in_category.grid(row=6, column=2, sticky="w")

    categories_lst = pars.make_categories_lst()
    category_combobox = ttk.Combobox(values=categories_lst, state="readonly")
    category_combobox.grid(row=6, column=1, sticky="w")
    category_combobox.bind("<<ComboboxSelected>>", category_combobox_selected)

    items_in_category = Label(text="", font=6)

    filters_label = Label(text="Set Filters: ", font=12)
    filters_label.grid(row=7, column=0)

    filters_button = ttk.Button(text="Submit", command=lambda: make_filters_window(pars))
    filters_button.grid(row=7, column=1, sticky="w")

    file_format_label = Label(text="Choose\nFile Format: ", font=12)
    file_format_label.grid(row=8, column=0)

    def file_format_combobox_selected(event):
        pars.set_file_format(file_format_combobox.get())
        start_scraping_button["state"] = "active"

    file_format_lst = ["json", "excel"]
    file_format_combobox = ttk.Combobox(values=file_format_lst, state="readonly")
    file_format_combobox.grid(row=8, column=1, sticky="w")
    file_format_combobox.bind("<<ComboboxSelected>>", file_format_combobox_selected)

    start_scraping_button = ttk.Button(text="Start Scraping", command=lambda: pars.save_cards(), state=["disabled"])
    start_scraping_button.grid(row=9, column=1)

    root.mainloop()

def make_filters_window(parser):
    filters_window = Tk()
    filters_window.title("Filters")
    filters_window.geometry("500x370")
    filters_window.resizable(False, False)

    # Condition
    def set_condition_filter():
        parser.set_filters("LH_ItemCondition", condition_var.get())
        print(parser.params)

    def condition_filter_del():
        del parser.params["LH_ItemCondition"]
        print(parser.params)

    def make_condition_buttons_active():
        condition_filter_submit_button["state"] = "active"
        condition_filter_delete_button["state"] = "active"

    condition_label = Label(filters_window,text="Condition: ", font=12)
    condition_label.grid(row=0, column=0, sticky="w")

    condition_var = StringVar(filters_window)

    condition_new = ttk.Radiobutton(filters_window, text="New", value="3", variable=condition_var, command=make_condition_buttons_active)
    condition_new.grid(row=0, column=1, sticky="w")

    condition_used = ttk.Radiobutton(filters_window, text="Used", value="4", variable=condition_var, command=make_condition_buttons_active)
    condition_used.grid(row=0, column=2, sticky="w")

    condition_filter_submit_button = ttk.Button(filters_window, text="Submit", command=set_condition_filter, state=["disabled"])
    condition_filter_submit_button.grid(row=0, column=3, sticky="w")

    condition_filter_delete_button = ttk.Button(filters_window, text="Delete", command=condition_filter_del, state=["disabled"])
    condition_filter_delete_button.grid(row=0, column=4, sticky="w")

    # Price
    price_label = Label(filters_window,text="Price: ", font=12)
    price_label.grid(row=1, column=0, sticky="w", pady=10)

    def set_min_price():
        parser.set_filters("_udlo", price_min_entry.get())
        print(parser.params)


    def delete_min_pirce():
        del parser.params["_udlo"]
        price_min_entry.delete(0, END)
        print(parser.params)

    price_min_label = Label(filters_window, text="Min: ")
    price_min_label.grid(row=1, column=1, sticky="w")

    price_min_entry = Entry(filters_window, width=10)
    price_min_entry.grid(row=1, column=2, sticky="w")

    price_min_submit_button = ttk.Button(filters_window, text="Submit", command=set_min_price)
    price_min_submit_button.grid(row=1, column=3, sticky="w")

    price_min_delete_button = ttk.Button(filters_window, text="Delete", command=delete_min_pirce)
    price_min_delete_button.grid(row=1, column=4, sticky="w")

    def set_max_price():
        parser.set_filters("_udhi", price_max_entry.get())
        print(parser.params)

    def delete_max_pirce():
        del parser.params["_udhi"]
        price_max_entry.delete(0, END)
        print(parser.params)

    price_max_label = Label(filters_window, text="Max: ")
    price_max_label.grid(row=2, column=1, sticky="w")

    price_max_entry = Entry(filters_window, width=10)
    price_max_entry.grid(row=2, column=2, sticky="w")

    price_max_submit_button = ttk.Button(filters_window, text="Submit", command=set_max_price)
    price_max_submit_button.grid(row=2, column=3, sticky="w")

    price_max_delete_button = ttk.Button(filters_window, text="Delete", command=delete_max_pirce)
    price_max_delete_button.grid(row=2, column=4, sticky="w")

    # Buying Format
    def set_buying_format_filter():
        buying_format_filter_del()
        value = buying_format_var.get()

        if "All" in value:
            name, val = value.split("=")
            parser.params[name] = val
        elif "Auction" in value:
            name, val = value.split("=")
            parser.params[name] = val
        elif "BIN" in value:
            name, val = value.split("=")
            parser.params[name] = val
        elif "BO" in value:
            name, val = value.split("=")
            parser.params[name] = val


    def buying_format_filter_del():
        if "LH_All" in parser.params:
            del parser.params["LH_All"]
        elif "LH_Auction" in parser.params:
            del parser.params["LH_Auction"]
        elif "LH_BIN" in parser.params:
            del parser.params["LH_BIN"]
        elif "LH_BO" in parser.params:
            del parser.params["LH_BO"]

    def make_buying_format_buttons_active():
        buying_format_filter_submit_button["state"] = "active"
        buying_format_filter_delete_button["state"] = "active"

    buying_format_label = Label(filters_window,text="Buying Format: ", font=12)
    buying_format_label.grid(row=3, column=0, sticky="w", pady=10)

    buying_format_var = StringVar(filters_window)

    buying_format_all = ttk.Radiobutton(filters_window, text="All listings", value="LH_All=1", variable=buying_format_var, command=make_buying_format_buttons_active)
    buying_format_all.grid(row=3, column=1, sticky="w")

    buying_format_auc = ttk.Radiobutton(filters_window, text="Auction", value="LH_Auction=1", variable=buying_format_var, command=make_buying_format_buttons_active)
    buying_format_auc.grid(row=3, column=2, sticky="w")

    buying_format_bin = ttk.Radiobutton(filters_window, text="Buy It Now", value="LH_BIN=1", variable=buying_format_var, command=make_buying_format_buttons_active)
    buying_format_bin.grid(row=4, column=1, sticky="w")

    buying_format_bo = ttk.Radiobutton(filters_window, text="Accepts Offers", value="LH_BO=1", variable=buying_format_var, command=make_buying_format_buttons_active)
    buying_format_bo.grid(row=4, column=2, sticky="w")

    buying_format_filter_submit_button = ttk.Button(filters_window, text="Submit", command=set_buying_format_filter, state=["disabled"])
    buying_format_filter_submit_button.grid(row=3, column=3, sticky="w")

    buying_format_filter_delete_button = ttk.Button(filters_window, text="Delete", command=buying_format_filter_del, state=["disabled"])
    buying_format_filter_delete_button.grid(row=3, column=4, sticky="w")

    # Item Location

    def set_item_Location_filter():
        parser.set_filters("LH_PrefLoc", item_Location_var.get())
        print(parser.params)

    def item_Location_filter_del():
        del parser.params["LH_PrefLoc"]
        print(parser.params)

    def make_item_Location_buttons_active():
        item_Location_filter_submit_button["state"] = "active"
        item_Location_filter_delete_button["state"] = "active"

    item_Location_label = Label(filters_window,text="Item Location: ", font=12)
    item_Location_label.grid(row=5, column=0, sticky="w", pady=10)

    item_Location_var = StringVar(filters_window)

    item_Location_default = ttk.Radiobutton(filters_window, text="Default", value="98", variable=item_Location_var, command=make_item_Location_buttons_active)
    item_Location_default.grid(row=5, column=1, sticky="w")

    item_Location_us = ttk.Radiobutton(filters_window, text="US Only", value="3", variable=item_Location_var, command=make_item_Location_buttons_active)
    item_Location_us.grid(row=5, column=2, sticky="w")

    item_Location_na = ttk.Radiobutton(filters_window, text="North America", value="4", variable=item_Location_var, command=make_item_Location_buttons_active)
    item_Location_na.grid(row=6, column=1, sticky="w")

    item_Location_eu = ttk.Radiobutton(filters_window, text="Europe", value="5", variable=item_Location_var, command=make_item_Location_buttons_active)
    item_Location_eu.grid(row=6, column=2, sticky="w")

    item_Location_asia = ttk.Radiobutton(filters_window, text="Asia", value="6", variable=item_Location_var, command=make_item_Location_buttons_active)
    item_Location_asia.grid(row=6, column=3, sticky="w")

    item_Location_filter_submit_button = ttk.Button(filters_window, text="Submit", command=set_item_Location_filter, state=["disabled"])
    item_Location_filter_submit_button.grid(row=5, column=3, sticky="w")

    item_Location_filter_delete_button = ttk.Button(filters_window, text="Delete", command=item_Location_filter_del, state=["disabled"])
    item_Location_filter_delete_button.grid(row=5, column=4, sticky="w")

    # Show Only

    show_only_label = Label(filters_window, text="Show Only: ", font=12)
    show_only_label.grid(row=7, column=0, sticky="w", pady=5)


    show_only_fr_var = IntVar(filters_window, value=0)
    show_only_default = ttk.Checkbutton(filters_window, text="Free Returns", variable=show_only_fr_var,
                                        command=lambda: parser.set_filters("LH_FR", str(show_only_fr_var.get())))
    show_only_default.grid(row=7, column=1, sticky="w")

    show_only_rpa_var = IntVar(filters_window, value=0)
    show_only_rpa = ttk.Checkbutton(filters_window, text="Returns Accepted", variable=show_only_rpa_var,
                                        command=lambda: parser.set_filters("LH_RPA", str(show_only_rpa_var.get())))
    show_only_rpa.grid(row=7, column=2, sticky="w")

    show_only_as_var = IntVar(filters_window, value=0)
    show_only_as = ttk.Checkbutton(filters_window, text="Auth. Seller", variable=show_only_as_var,
                                    command=lambda: parser.set_filters("LH_AS", str(show_only_as_var.get())))
    show_only_as.grid(row=7, column=3, sticky="w")

    show_only_ci_var = IntVar(filters_window, value=0)
    show_only_ci = ttk.Checkbutton(filters_window, text="Comp. Items", variable=show_only_ci_var,
                                   command=lambda: parser.set_filters("LH_Complete", str(show_only_ci_var.get())))
    show_only_ci.grid(row=8, column=1, sticky="w", pady=5)

    show_only_sd_var = IntVar(filters_window, value=0)
    show_only_sd = ttk.Checkbutton(filters_window, text="Sold Items", variable=show_only_sd_var,
                                   command=lambda: parser.set_filters("LH_Sold", str(show_only_sd_var.get())))
    show_only_sd.grid(row=8, column=2, sticky="w")

    show_only_ds_var = IntVar(filters_window, value=0)
    show_only_ds = ttk.Checkbutton(filters_window, text="Deals & Savings", variable=show_only_ds_var,
                                   command=lambda: parser.set_filters("LH_Savings", str(show_only_ds_var.get())))
    show_only_ds.grid(row=9, column=1, sticky="w", pady=5)

    show_only_av_var = IntVar(filters_window, value=0)
    show_only_av = ttk.Checkbutton(filters_window, text="Auth. Guarantee", variable=show_only_av_var,
                                   command=lambda: parser.set_filters("LH_AV", str(show_only_av_var.get())))
    show_only_av.grid(row=9, column=2, sticky="w")

    filters_window.mainloop()
def main():
    make_started_window()
