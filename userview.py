import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
from datetime import datetime

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
        self.donor_id = tk.StringVar()#it holds the data
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
#used to set up gui components
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
#input field for user data entry
    def create_entry_widgets(self):
        labels = ["Name", "Donor ID", "Blood Group", "Contact No", "Age", "Donation Date", "Address"]
        variables = [self.name, self.donor_id, self.blood_group, self.contact, self.age, self.donation_date, self.address]

        for i, (label_text, var) in enumerate(zip(labels, variables)):
            tk.Label(self.frame_details, text=label_text, font=("Times new roman", 17), bg="white").grid(row=i,column=0,padx=2,pady=2)
            tk.Entry(self.frame_details, bd=7, font=("Times new roman", 17), width=17, textvariable=var).grid(row=i,column=1, padx=2,pady=2)

    def create_buttons(self):
        btn_frame = tk.Frame(self.frame_details, bg="white", bd=7, relief=tk.GROOVE)
        btn_frame.place(x=15, y=390, width=348, height=120)
#when user click this button this function is triggered
        tk.Button(btn_frame, text="Add", bg="white", font=("Times new roman", 15), width=10,
                  command=self.add_data).grid(row=0, column=0, padx=100, pady=25)
#user can search by diff criteria
    def create_search_frame(self):
        search_frame = tk.Frame(self.frame_data, bg="white", bd=10, relief=tk.GROOVE)
        search_frame.pack(side=tk.TOP, fill=tk.X)

        tk.Label(search_frame, text="Search By", bg="white", font=("Times new roman", 16)).grid(row=0, column=0,
                                                                                               padx=12, pady=2)
#comb to select dif criteria
        search_combobox = ttk.Combobox(search_frame, font=("Times new roman", 16), state="readonly",
                                       textvariable=self.search_criteria)
        search_combobox['values'] = ("Name", "Donor ID", "Blood Group", "Contact No", "Age", "Donation Date")
        search_combobox.grid(row=0, column=1, padx=12, pady=2)

        tk.Label(search_frame, text="Search Value", bg="white", font=("Times new roman", 16)).grid(row=0, column=2,
                                                                                                 padx=12, pady=2)

        tk.Entry(search_frame, font=("Times new roman", 16), textvariable=self.search_value).grid(row=0, column=3,
                                                                                              padx=12, pady=2)

        tk.Button(search_frame, text="Search", bg="white", font=("Times new roman", 15), width=14,
                  command=self.search_data).grid(row=0, column=4, padx=12, pady=2)
#to create using tree view widget to display donor rec0rd
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
#establosh connection using pymysql.connect
    def db_connect(self):
        try:
            return pymysql.connect(**self.db_params)
        except pymysql.MySQLError as e:
            messagebox.showerror("Database Error", f"Could not connect to database: {e}")

            return None
#used to fetch all the donor records from db
    def load_data(self):
        con = self.db_connect()
        if con:
            try:
                #to execute qurey we use cursor object
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

    def validate_contact(self, contact):
        """Validate if the contact number is exactly 10 digits long."""
        return contact.isdigit() and len(contact) == 10
#insert the donor details
    def add_data(self):
        # Validate individual fields
        if self.donor_id.get() == "":
            messagebox.showerror('Error', 'Donor ID is required')
            return
        if self.name.get() == "":
            messagebox.showerror('Error', 'Name is required')
            return
        if self.blood_group.get() == "":
            messagebox.showerror('Error', 'Blood Group is required')
            return
        if self.contact.get() == "":
            messagebox.showerror('Error', 'Contact number is required')
            return
        if not self.validate_contact(self.contact.get()):
            messagebox.showerror('Error', 'Contact number must be exactly 10 digits')
            return
        if self.age.get() == "":
            messagebox.showerror('Error', 'Age is required')
            return
        if not self.age.get().isdigit() or int(self.age.get()) <= 0:
            messagebox.showerror('Error', 'Age must be a positive integer')
            return
        if self.address.get() == "":
            messagebox.showerror('Error', 'Address is required')
            return

        # Set current date if donation date is not provided
        if self.donation_date.get() == "":
            self.donation_date.set(datetime.now().strftime('%Y-%m-%d'))

        # Connect to the database and insert data
        con = self.db_connect()
        if con:
            try:
                with con.cursor() as cur:
                    cur.execute(
                        "INSERT INTO donors (donor_id, name, blood_group, contact, age, donation_date, address) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (self.donor_id.get(), self.name.get(), self.blood_group.get(), self.contact.get(),
                         self.age.get(), self.donation_date.get(), self.address.get()))
                    con.commit()
                    # Reload the data in the table
                    self.load_data()
                    # Clear the input fields
                    self.clear_entries()
                    # Show success message
                    messagebox.showinfo("Success", "Record has been saved successfully")
            except pymysql.MySQLError as e:
                # Show detailed database error message
                messagebox.showerror("Database Error", f"Error while adding data: {e}")
            except Exception as e:
                # Show general error message
                messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            finally:
                # Ensure the connection is closed
                con.close()

    def clear_entries(self):
        """Clear all entry fields."""
        for var in [self.donor_id, self.name, self.blood_group, self.contact, self.age, self.address]:
            var.set('')
        self.donation_date.set('')

    def focus_item(self, event):
        """Populate entry fields with selected table item data."""
        selected_item = self.donor_table.focus()
        if selected_item:
            item_data = self.donor_table.item(selected_item, 'values')
            if item_data:
                self.donor_id.set(item_data[0])
                self.name.set(item_data[1])
                self.blood_group.set(item_data[2])
                self.contact.set(item_data[3])
                self.age.set(item_data[4])
                self.donation_date.set(item_data[5])
                self.address.set(item_data[6])


# Create and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = BloodDonationApp(root)
    root.mainloop()
