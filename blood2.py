import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
from datetime import datetime  # Import datetime module


class BloodDonationApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700")
        self.root.title("Blood Donation Management")

        # Database connection parameters
        self.db_params = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'blood_donors'
        }

        # Initialize variables
        self.donor_id = tk.StringVar()
        self.name = tk.StringVar()
        self.blood_group = tk.StringVar()
        self.contact = tk.StringVar()
        self.age = tk.StringVar()
        self.donation_date = tk.StringVar()
        self.address = tk.StringVar()
        self.search_criteria = tk.StringVar()
        self.search_value = tk.StringVar()

        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        # Header
        tk.Label(self.root, text="Blood Donation Management", font=("Times new roman", 35, "bold"),
                 bg="white", fg="black", border=12, relief=tk.GROOVE).pack(side=tk.TOP, fill=tk.X)

        # Frames
        self.frame_details = tk.LabelFrame(self.root, text="Enter details", font=("Times new roman", 22, "bold"),
                                           bd=12, relief=tk.GROOVE, bg="white")
        self.frame_details.place(x=20, y=100, width=400, height=575)

        self.frame_data = tk.Frame(self.root, bd=12, relief=tk.GROOVE, bg="white")
        self.frame_data.place(x=440, y=100, width=1100, height=575)

        # Entry widgets
        self.create_entry_widgets()

        # Buttons
        self.create_buttons()

        # Search Frame
        self.create_search_frame()

        # Data Table
        self.create_data_table()

    def create_entry_widgets(self):
        labels = ["Name", "Donor ID", "Blood Group", "Contact No", "Age", "Donation Date", "Address"]
        variables = [self.name, self.donor_id, self.blood_group, self.contact, self.age, self.donation_date,
                     self.address]

        for i, (label_text, var) in enumerate(zip(labels, variables)):
            tk.Label(self.frame_details, text=label_text, font=("Times new roman", 17), bg="white").grid(row=i, column=0,padx=2, pady=2)
            tk.Entry(self.frame_details, bd=7, font=("Times new roman", 17), width=17, textvariable=var).grid(row=i,column=1,padx=2,pady=2)

    def create_buttons(self):
        btn_frame = tk.Frame(self.frame_details, bg="white", bd=7, relief=tk.GROOVE)
        btn_frame.place(x=15, y=390, width=348, height=120)

        tk.Button(btn_frame, text="Add", bg="white", font=("Times new roman", 15), width=13,
                  command=self.add_data).grid(row=0, column=0, padx=2, pady=2)
        tk.Button(btn_frame, text="Delete", bg="white", font=("Times new roman", 15), width=13,
                  command=self.delete_data).grid(row=0, column=1, padx=2, pady=2)
        tk.Button(btn_frame, text="Update", bg="white", font=("Times new roman", 15), width=13,
                  command=self.update_data).grid(row=1, column=0, padx=2, pady=2)
        tk.Button(btn_frame, text="Clear", bg="white", font=("Times new roman", 15), width=13,
                  command=self.clear_entries).grid(row=1, column=1, padx=2, pady=2)

    def create_search_frame(self):
        search_frame = tk.Frame(self.frame_data, bg="white", bd=10, relief=tk.GROOVE)
        search_frame.pack(side=tk.TOP, fill=tk.X)

        tk.Label(search_frame, text="Search By", bg="white", font=("Times new roman", 16)).grid(row=0, column=0,padx=12, pady=2)

        search_combobox = ttk.Combobox(search_frame, font=("Times new roman", 16), state="readonly",
                                       textvariable=self.search_criteria)
        search_combobox['values'] = ("Name", "Donor ID", "Blood Group", "Contact No", "Age", "Donation Date")
        search_combobox.grid(row=0, column=1, padx=12, pady=2)

        tk.Label(search_frame, text="Search Value", bg="white", font=("Times new roman", 16)).grid(row=0, column=2,padx=12, pady=2)

        tk.Entry(search_frame, font=("Times new roman", 16), textvariable=self.search_value).grid(row=0, column=3,padx=12, pady=2)

        tk.Button(search_frame, text="Search", bg="white", font=("Times new roman", 15), width=14,
                  command=self.search_data).grid(row=0, column=4, padx=12, pady=2)

    def create_data_table(self):
        db_frame = tk.Frame(self.frame_data, bg="white", bd=11, relief=tk.GROOVE)
        db_frame.pack(fill=tk.BOTH, expand=True)

        scroll_x = tk.Scrollbar(db_frame, orient=tk.HORIZONTAL)
        scroll_y = tk.Scrollbar(db_frame, orient=tk.VERTICAL)

        self.donor_table = ttk.Treeview(db_frame, columns=(
        "Donor ID", "Name", "Blood Group", "Contact No", "Age", "Donation Date", "Address"),
                                        yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_x.config(command=self.donor_table.xview)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        scroll_y.config(command=self.donor_table.yview)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.donor_table.heading("Donor ID", text="Donor ID")
        self.donor_table.heading("Name", text="Name")
        self.donor_table.heading("Blood Group", text="Blood Group")
        self.donor_table.heading("Contact No", text="Contact No")
        self.donor_table.heading("Age", text="Age")
        self.donor_table.heading("Donation Date", text="Donation Date")
        self.donor_table.heading("Address", text="Address")

        self.donor_table['show'] = 'headings'
        self.donor_table.column("Donor ID", width=100)
        self.donor_table.column("Name", width=100)
        self.donor_table.column("Blood Group", width=100)
        self.donor_table.column("Contact No", width=100)
        self.donor_table.column("Age", width=100)
        self.donor_table.column("Donation Date", width=100)
        self.donor_table.column("Address", width=150)

        self.donor_table.pack(fill=tk.BOTH, expand=True)
        self.donor_table.bind("<ButtonRelease-1>", self.focus_item)

    def db_connect(self):
        try:
            return pymysql.connect(**self.db_params)
        except pymysql.MySQLError as e:
            messagebox.showerror("Database Error", f"Could not connect to database: {e}")
            return None

    def load_data(self):
        con = self.db_connect()
        if con:
            try:
                with con.cursor() as cur:
                    cur.execute('SELECT * FROM donors')
                    rows = cur.fetchall()
                    if rows:
                        self.donor_table.delete(*self.donor_table.get_children())
                        for row in rows:
                            self.donor_table.insert('', tk.END, values=row)
            except Exception as e:
                messagebox.showerror("Error", f"Error while fetching data: {e}")
            finally:
                con.close()

    def search_data(self):
        criteria = self.search_criteria.get()
        value = self.search_value.get()

        if criteria == "" or value == "":
            messagebox.showerror("Error", "Please select a search criterion and enter a value")
            return

        column_map = {
            "Name": "name",
            "Donor ID": "donor_id",
            "Blood Group": "blood_group",
            "Contact No": "contact",
            "Age": "age",
            "Donation Date": "donation_date"
        }

        column_name = column_map.get(criteria)

        con = self.db_connect()
        if con:
            try:
                with con.cursor() as cur:
                    query = f"SELECT * FROM donors WHERE {column_name} LIKE %s"
                    cur.execute(query, (f'%{value}%',))
                    rows = cur.fetchall()
                    if rows:
                        self.donor_table.delete(*self.donor_table.get_children())
                        for row in rows:
                            self.donor_table.insert('', tk.END, values=row)
                    else:
                        self.donor_table.delete(*self.donor_table.get_children())
                        messagebox.showinfo("No Results", "No records found matching your criteria.")
            except Exception as e:
                messagebox.showerror("Error", f"Error while searching data: {e}")
            finally:
                con.close()
    def add_data(self):
        if any(v.get() == "" for v in [self.donor_id, self.name, self.blood_group,self.age,self.address,self.contact]):
            messagebox.showerror('Error', 'All Fields required')
        else:
            if self.donation_date.get() == "":
                self.donation_date.set(datetime.now().strftime('%Y-%m-%d'))  # Set current date if not provided
            con = self.db_connect()
            if con:
                try:
                    with con.cursor() as cur:
                        cur.execute(
                            "INSERT INTO donors (donor_id, name, blood_group, contact, age, donation_date, address) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                            (self.donor_id.get(), self.name.get(), self.blood_group.get(), self.contact.get(),
                             self.age.get(), self.donation_date.get(), self.address.get()))
                        con.commit()
                        self.load_data()
                        self.clear_entries()
                        messagebox.showinfo("Success", "Record has been saved successfully")
                except Exception as e:
                    messagebox.showerror("Error", f"Error while adding data: {e}")
                finally:
                    con.close()
    def update_data(self):
        if any(v.get() == "" for v in [self.donor_id, self.name, self.blood_group, self.age, self.address, self.contact]):
            messagebox.showerror('Error', 'All Fields required')
        else:
            if self.donation_date.get() == "":
                self.donation_date.set(datetime.now().strftime('%Y-%m-%d'))  # Set current date if not provided
            con = self.db_connect()
            if con:
                try:
                    with con.cursor() as cur:
                        cur.execute(
                            "UPDATE donors SET name=%s, blood_group=%s, contact=%s, age=%s, donation_date=%s, address=%s WHERE donor_id=%s",
                            (self.name.get(), self.blood_group.get(), self.contact.get(), self.age.get(),
                            self.donation_date.get(), self.address.get(), self.donor_id.get()))
                        con.commit()
                        self.load_data()
                        self.clear_entries()
                        messagebox.showinfo("Success", "Record updated successfully")
                except Exception as e:
                    messagebox.showerror("Error", f"Error while updating data: {e}")
                finally:
                    con.close()

    def delete_data(self):
        if any(v.get() == "" for v in [self.donor_id, self.name, self.blood_group, self.age, self.address, self.contact]):
            messagebox.showerror('Error', 'All Fields required')
        else:
            con = self.db_connect()
            if con:
                try:
                    with con.cursor() as cur:
                        cur.execute('DELETE FROM donors WHERE donor_id=%s', (self.donor_id.get(),))
                        con.commit()
                        self.load_data()
                        self.clear_entries()
                        messagebox.showinfo('Success', 'Record has been deleted')
                except Exception as e:
                    messagebox.showerror("Error", f"Error while deleting data: {e}")
                finally:
                    con.close()

    def clear_entries(self):
        self.donor_id.set("")
        self.name.set("")
        self.blood_group.set("")
        self.contact.set("")
        self.age.set("")
        self.donation_date.set("")
        self.address.set("")

    def focus_item(self, event):
        selected_item = self.donor_table.focus()
        if selected_item:
            row = self.donor_table.item(selected_item)['values']
            self.donor_id.set(row[0])
            self.name.set(row[1])
            self.blood_group.set(row[2])
            self.contact.set(row[3])
            self.age.set(row[4])
            self.donation_date.set(row[5])
            self.address.set(row[6])


if __name__ == "__main__":
    root = tk.Tk()
    app = BloodDonationApp(root)
    root.mainloop()
