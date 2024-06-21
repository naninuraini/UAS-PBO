import tkinter as tk
from tkinter import messagebox
import pymysql
import datetime
import uuid

now = datetime.datetime.now()
odate = now.strftime("%y-%m-%d")
otime = now.strftime("%H:%M:%S")

class bill():
    def __init__(self, root):
        self.root = root
        self.root.title("Watro.nila Billing System")

        scrn_width = self.root.winfo_screenwidth()
        scrn_height = self.root.winfo_screenheight()

        self.root.geometry("1060x600")

        mainTitle = tk.Label(self.root, text="Watro.nila Billing System", bg="purple", fg="white", bd=5, relief="groove", font=("Arial", 40, "bold"))
        mainTitle.pack(side="top", fill="x")

        # -----Global Variables-------------
        self.total = tk.IntVar()
        self.satu = 1

        # -----input Frame-------------
        self.inputFrame = tk.Frame(self.root, bg="purple", bd=5, relief="groove")
        self.inputFrame.pack(side="left", fill="y")

        itemLabel = tk.Label(self.inputFrame, text="Item Name:", bg="purple", font=("Arial", 18, "bold"))
        itemLabel.grid(row=0, column=0, padx=10, pady=30)
        self.itemIn = tk.Entry(self.inputFrame, width=15, font=("Arial", 18))
        self.itemIn.grid(row=0, column=1, padx=5, pady=30)

        quantLabel = tk.Label(self.inputFrame, text="Item Quantity:", bg="purple", font=("Arial", 18, "bold"))
        quantLabel.grid(row=1, column=0, padx=10, pady=30)
        self.quantIn = tk.Entry(self.inputFrame, width=15, font=("Arial", 18))
        self.quantIn.grid(row=1, column=1, padx=5, pady=30)

        purchaseBtn = tk.Button(self.inputFrame, width=8, command=self.purchase, text="Purchase", bg="light gray", bd=2, relief="raised", font=("Arial", 20, "bold"))
        purchaseBtn.grid(row=2, column=0, padx=30, pady=50)

        printBillBtn = tk.Button(self.inputFrame, width=8, command=self.print_bill, text="Print Bill", bg="light gray", bd=2, relief="raised", font=("Arial", 20, "bold"))
        printBillBtn.grid(row=2, column=1, padx=30, pady=50)

        addBtn = tk.Button(self.inputFrame, width=15, command=self.add_fun, text="Add Item", bg="light gray", bd=2, relief="raised", font=("Arial", 20, "bold"))
        addBtn.grid(row=3, column=0, padx=30, pady=20, columnspan=2)

        clearBtn = tk.Button(self.inputFrame, width=15, command=self.clear_bill, text="Clear Bill", bg="light gray", bd=2, relief="raised", font=("Arial", 20, "bold"))
        clearBtn.grid(row=4, column=0, padx=30, pady=20, columnspan=2)

        # -----Detail Frame-------------
        self.detailFrame = tk.Frame(self.root, bg="purple", bd=5, relief="groove")
        self.detailFrame.pack(fill="both", expand=True)

        self.list = tk.Listbox(self.detailFrame, width=68, height=27, bg="pink", bd=3, relief="sunken", font=("Arial", 15))
        self.list.grid(row=0, column=0, padx=20, pady=20)

    def add_fun(self):
        self.addFrame = tk.Frame(self.root, bg="sky blue", bd=5, relief="groove")
        self.addFrame.place(x=395, y=60, width=450, height=538)

        itemLabel = tk.Label(self.addFrame, text="Item Name:", bg="sky blue", font=("Arial", 18, "bold"))
        itemLabel.grid(row=0, column=0, padx=10, pady=30)
        self.itemIn = tk.Entry(self.addFrame, width=15, font=("Arial", 18))
        self.itemIn.grid(row=0, column=1, padx=5, pady=30)

        priceLabel = tk.Label(self.addFrame, text="Item Price:", bg="sky blue", font=("Arial", 18, "bold"))
        priceLabel.grid(row=1, column=0, padx=10, pady=30)
        self.priceIn = tk.Entry(self.addFrame, width=15, font=("Arial", 18))
        self.priceIn.grid(row=1, column=1, padx=5, pady=30)

        quantLabel = tk.Label(self.addFrame, text="Item Quantity:", bg="sky blue", font=("Arial", 18, "bold"))
        quantLabel.grid(row=2, column=0, padx=10, pady=30)
        self.quantIn = tk.Entry(self.addFrame, width=15, font=("Arial", 18))
        self.quantIn.grid(row=2, column=1, padx=5, pady=30)

        okBtn = tk.Button(self.addFrame, width=8, command=self.insert_Fun, text="Ok", bg="light gray", bd=2, relief="raised", font=("Arial", 20, "bold"))
        okBtn.grid(row=3, column=0, padx=30, pady=50)

        closeBtn = tk.Button(self.addFrame, width=8, command=self.close, text="Close", bg="light gray", bd=2, relief="raised", font=("Arial", 20, "bold"))
        closeBtn.grid(row=3, column=1, padx=30, pady=50)

    def insert_Fun(self):
        itemName = self.itemIn.get()
        itemPrice = int(self.priceIn.get())
        itemQuant = int(self.quantIn.get())

        con = pymysql.connect(host="localhost", user="root", passwd="", database="marketdb")
        cur = con.cursor()

        # Check if item with same name and price exists
        cur.execute("SELECT * FROM item WHERE item_name = %s AND item_price = %s", (itemName, itemPrice))
        existing_item = cur.fetchone()

        if existing_item:
            # If item exists, update quantity
            new_quantity = existing_item[2] + itemQuant
            cur.execute("UPDATE item SET item_quant = %s WHERE item_name = %s AND item_price = %s", (new_quantity, itemName, itemPrice))
        else:
            # If item does not exist, insert new item
            cur.execute("INSERT INTO item (item_name, item_price, item_quant) VALUES (%s, %s, %s)", (itemName, itemPrice, itemQuant))

        con.commit()
        tk.messagebox.showinfo("Success", "Item Added Successfully!")
        self.clear_add()
        con.close()

    def clear_add(self):
        self.itemIn.delete(0, tk.END)
        self.priceIn.delete(0, tk.END)
        self.quantIn.delete(0, tk.END)

    def close(self):
        self.addFrame.destroy()

    def clear_bill(self):
        self.list.delete(0, tk.END)
        self.total.set(0)
        self.satu = 1

    def purchase(self):
        item = self.itemIn.get()
        quantity = int(self.quantIn.get())

        con = pymysql.connect(host="localhost", user="root", passwd="", database="marketdb")
        cur = con.cursor()
        cur.execute("SELECT item_price, item_quant FROM item WHERE item_name=%s", (item,))
        data = cur.fetchone()

        if self.satu == 1:
            joedoel = "                Welcome to Himatro Unila Market            "
            dati = f"Date: {odate}                                           {otime}"
            aidi = uuid.uuid1().int >> 64
            nums = f"Bill number: {aidi}"
            stroek1 = "=" * 60
            stroek2 = "Name           Quantity         Price           Amount"
            stroek3 = "=" * 60
            self.list.insert(tk.END, joedoel)
            self.list.insert(tk.END, dati)
            self.list.insert(tk.END, nums)
            self.list.insert(tk.END, stroek1)
            self.list.insert(tk.END, stroek2)
            self.list.insert(tk.END, stroek3)

        if data:
            if data[1] >= quantity:
                price = data[0]
                amount = price * quantity
                self.total.set(self.total.get() + amount)
                update = data[1] - quantity
                cur.execute("UPDATE item SET item_quant=%s WHERE item_name=%s", (update, item))
                con.commit()
                con.close()
                info = f"{item:<15} {quantity:<15} {price:<15} {amount:<15}"
                self.satu = 0
                self.list.insert(tk.END, info)
                self.clearInput()
            else:
                tk.messagebox.showerror("Error", "Not Enough Quantity!")
                self.clearInput()
        else:
            tk.messagebox.showerror("Error", "Item Not Found!")
            self.clearInput()

    def print_bill(self):
        if self.list.size() == 0:
            tk.messagebox.showwarning("No Items", "No items have been added to the bill.")
        else:
            line = "=" * 60
            printBill = f"Total Bill: {self.total.get()}"
            self.list.insert(tk.END, line)
            self.list.insert(tk.END, printBill)

    def clearInput(self):
        self.itemIn.delete(0, tk.END)
        self.quantIn.delete(0, tk.END)

root = tk.Tk()
obj = bill(root)
root.mainloop()
