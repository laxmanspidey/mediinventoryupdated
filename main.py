import streamlit as st
import pandas as pd
from PIL import Image
import random
import sqlite3
import os

# Database Connection
conn = sqlite3.connect("drug_data.db", check_same_thread=False)
c = conn.cursor()

# Custom CSS for Styling
'''
st.markdown(
    """
    <style>
    /* Main Title */
    .main-title {
        font-size: 36px;
        font-weight: bold;
        color: #FF5733; /* Changed color */
        text-align: center;
        margin-bottom: 20px;
    }

    /* Sidebar Styling */
    .sidebar .sidebar-content {
        background-color: #4A90E2; /* Changed color */
        color: white;
        padding: 20px;
    }

    .sidebar .sidebar-content .sidebar-title {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
    }

    .sidebar .sidebar-content .sidebar-text {
        font-size: 16px;
        margin-bottom: 20px;
    }

    /* Button Styling */
    .stButton button {
        background-color: #34A853; /* Changed color */
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;
        border: none;
    }

    .stButton button:hover {
        background-color: #2E8B57; /* Changed hover color */
    }

    /* Expander Styling */
    .stExpander {
        background-color: #1E1E1E; /* Dark background for expander */
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 20px;
        color: white; /* Text color inside expander */
    }

    /* DataFrame Styling */
    .stDataFrame {
        background-color: #1E1E1E !important; /* Dark background for table */
        color: white !important; /* Text color for table */
    }

    .stDataFrame th {
        background-color: #333333 !important; /* Dark gray for header */
        color: white !important;
    }

    .stDataFrame td {
        border: 1px solid #444444 !important; /* Border color for cells */
    }

    /* Footer Styling */
    .footer {
        font-size: 14px;
        text-align: center;
        margin-top: 40px;
        padding: 20px;
        background-color: #333333; /* Changed color */
        color: white;
        border-radius: 5px;
    }
    </style>

    MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)
'''

# Custom CSS for Styling
st.markdown(
    """
    <style>
    /* Main Title */
    .main-title {
        font-size: 36px;
        font-weight: bold;
        color: #FF5733; /* Changed color */
        text-align: center;
        margin-bottom: 20px;
    }

    /* Sidebar Styling */
    .sidebar .sidebar-content {
        background-color: #4A90E2; /* Changed color */
        color: white;
        padding: 20px;
    }

    .sidebar .sidebar-content .sidebar-title {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
    }

    .sidebar .sidebar-content .sidebar-text {
        font-size: 16px;
        margin-bottom: 20px;
    }

    /* Button Styling */
    .stButton button {
        background-color: #34A853; /* Changed color */
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;
        border: none;
    }

    .stButton button:hover {
        background-color: #2E8B57; /* Changed hover color */
    }

    /* Expander Styling */
    .stExpander {
        background-color: #1E1E1E; /* Dark background for expander */
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 20px;
        color: white; /* Text color inside expander */
    }

    /* DataFrame Styling */
    .stDataFrame {
        background-color: #1E1E1E !important; /* Dark background for table */
        color: white !important; /* Text color for table */
    }

    .stDataFrame th {
        background-color: #333333 !important; /* Dark gray for header */
        color: white !important;
    }

    .stDataFrame td {
        border: 1px solid #444444 !important; /* Border color for cells */
    }

    /* Footer Styling */
    .footer {
        font-size: 14px;
        text-align: center;
        margin-top: 40px;
        padding: 20px;
        background-color: #333333; /* Changed color */
        color: white;
        border-radius: 5px;
    }

    /* Hide Streamlit settings, share, and other options */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

def update_drug_quantity(drug_name, quantity_purchased):
    # Fetch the current quantity of the drug
    c.execute('SELECT D_Qty FROM Drugs WHERE D_Name = ?', (drug_name,))
    current_quantity = c.fetchone()[0]
    
    # Calculate the new quantity
    new_quantity = current_quantity - quantity_purchased
    
    # Update the drug quantity in the database
    c.execute('UPDATE Drugs SET D_Qty = ? WHERE D_Name = ?', (new_quantity, drug_name))
    conn.commit()

# Database Functions (unchanged)
def cust_create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS Customers(
                    C_Name VARCHAR(50) NOT NULL,
                    C_Password VARCHAR(50) NOT NULL,
                    C_Email VARCHAR(50) PRIMARY KEY NOT NULL, 
                    C_State VARCHAR(50) NOT NULL,
                    C_Number VARCHAR(50) NOT NULL 
                    )''')
    print('Customer Table created Successfully')

def customer_add_data(Cname, Cpass, Cemail, Cstate, Cnumber):
    c.execute('''INSERT INTO Customers (C_Name, C_Password, C_Email, C_State, C_Number) VALUES(?,?,?,?,?)''', 
              (Cname, Cpass, Cemail, Cstate, Cnumber))
    conn.commit()

def customer_view_all_data():
    c.execute('SELECT * FROM Customers')
    customer_data = c.fetchall()
    return customer_data

def customer_update(Cemail, Cnumber):
    c.execute('''UPDATE Customers SET C_Number = ? WHERE C_Email = ?''', (Cnumber, Cemail))
    conn.commit()
    print("Updating")

def customer_delete(Cemail):
    c.execute('''DELETE FROM Customers WHERE C_Email = ?''', (Cemail,))
    conn.commit()

def drug_update(Duse, Did):
    c.execute('''UPDATE Drugs SET D_Use = ? WHERE D_id = ?''', (Duse, Did))
    conn.commit()

def drug_delete(Did):
    c.execute('''DELETE FROM Drugs WHERE D_id = ?''', (Did,))
    conn.commit()

def drug_create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS Drugs(
                D_Name VARCHAR(50) NOT NULL,
                D_ExpDate DATE NOT NULL, 
                D_Use VARCHAR(50) NOT NULL,
                D_Qty INT NOT NULL, 
                D_id INT PRIMARY KEY NOT NULL)
                ''')
    print('DRUG Table created Successfully')

def drug_add_data(Dname, Dexpdate, Duse, Dqty, Did):
    c.execute('''INSERT INTO Drugs (D_Name, D_Expdate, D_Use, D_Qty, D_id) VALUES(?,?,?,?,?)''', 
              (Dname, Dexpdate, Duse, Dqty, Did))
    conn.commit()

def drug_view_all_data():
    c.execute('SELECT * FROM Drugs')
    drug_data = c.fetchall()
    return drug_data

def order_create_table():
    c.execute('''
        CREATE TABLE IF NOT EXISTS Orders(
                O_Name VARCHAR(100) NOT NULL,
                O_Items VARCHAR(100) NOT NULL,
                O_Qty VARCHAR(100) NOT NULL,
                O_id VARCHAR(100) PRIMARY KEY NOT NULL)
    ''')

def order_delete(Oid):
    c.execute('''DELETE FROM Orders WHERE O_id = ?''', (Oid,))

def order_add_data(O_Name, O_Items, O_Qty, O_id):
    c.execute('''INSERT INTO Orders (O_Name, O_Items, O_Qty, O_id) VALUES(?,?,?,?)''',
              (O_Name, O_Items, O_Qty, O_id))
    conn.commit()

def order_view_data(customername):
    c.execute('SELECT * FROM ORDERS WHERE O_Name == ?', (customername,))
    order_data = c.fetchall()
    return order_data

def order_view_all_data():
    c.execute('SELECT * FROM ORDERS')
    order_all_data = c.fetchall()
    return order_all_data

# Admin Function (unchanged)
def admin():
    st.title("Pharmacy Database Dashboard")
    st.subheader("Select an option from the menu to manage different aspects of the pharmacy database.")
    menu = ["Drugs", "Customers", "Orders", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Drugs":
        st.subheader("Manage Drugs")
        menu = ["Add", "View", "Update", "Delete"]
        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "Add":
            st.subheader("Add Drugs")
            col1, col2 = st.columns(2)
            with col1:
                drug_name = st.text_area("Enter the Drug Name")
                drug_expiry = st.date_input("Expiry Date of Drug (YYYY-MM-DD)")
                drug_mainuse = st.text_area("When to Use")
            with col2:
                drug_quantity = st.text_area("Enter the quantity")
                drug_id = st.text_area("Enter the Drug id (example:#D1)")
            if st.button("Add Drug"):
                drug_add_data(drug_name, drug_expiry, drug_mainuse, drug_quantity, drug_id)
                st.success("Successfully Added Data")
        if choice == "View":
            st.subheader("Drug Details")
            drug_result = drug_view_all_data()
            with st.expander("View All Drug Data"):
                drug_clean_df = pd.DataFrame(drug_result, columns=["Name", "Expiry Date", "Use", "Quantity", "ID"])
                st.dataframe(drug_clean_df)
            with st.expander("View Drug Quantity"):
                drug_name_quantity_df = drug_clean_df[['Name', 'Quantity']]
                st.dataframe(drug_name_quantity_df)
        if choice == 'Update':
            st.subheader("Update Drug Details")
            d_id = st.text_area("Drug ID")
            d_use = st.text_area("Drug Use")
            if st.button(label='Update'):
                drug_update(d_use, d_id)
        if choice == 'Delete':
            st.subheader("Delete Drugs")
            did = st.text_area("Drug ID")
            if st.button(label="Delete"):
                drug_delete(did)

    elif choice == "Customers":
        menu = ["View", "Update", "Delete"]
        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "View":
            st.subheader("Customer Details")
            cust_result = customer_view_all_data()
            with st.expander("View All Customer Data"):
                cust_clean_df = pd.DataFrame(cust_result, columns=["Name", "Password", "Email-ID", "Area", "Number"])
                st.dataframe(cust_clean_df)
        if choice == 'Update':
            st.subheader("Update Customer Details")
            cust_email = st.text_area("Email")
            cust_number = st.text_area("Phone Number")
            if st.button(label='Update'):
                customer_update(cust_email, cust_number)
        if choice == 'Delete':
            st.subheader("Delete Customer")
            cust_email = st.text_area("Email")
            if st.button(label="Delete"):
                customer_delete(cust_email)

    elif choice == "Orders":
        menu = ["View"]
        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "View":
            st.subheader("Order Details")
            order_result = order_view_all_data()
            with st.expander("View All Order Data", expanded=True):
                order_clean_df = pd.DataFrame(order_result, columns=["Name", "Items", "Qty", "ID"])
                st.dataframe(order_clean_df.style.set_properties(**{'font-size': '16px'}))
            st.subheader("Order Details (Expanded)")
            st.dataframe(order_clean_df.style.set_properties(**{'font-size': '16px'}))

    elif choice == "About":
        st.subheader("MIS Mini Project")
        st.subheader("By Laxman")

def getauthenicate(username, password):
    #print("Auth")
    c.execute('SELECT C_Password FROM Customers WHERE C_Name = ?', (username,))
    cust_password = c.fetchall()
    #print(cust_password[0][0], "Outside password")
    #print(password, "Parameter password")
    if cust_password[0][0] == password:
        #print("Inside password")
        return True
    else:
        return False

# Customer Function (unchanged)
import pillow_avif  # This enables AVIF support in Pillow

# def customer(username, password):
#     if getauthenicate(username, password):
#         st.title("Welcome to Pharmacy Store")
#         st.subheader("Your Order Details")
#         order_result = order_view_data(username)
#         with st.expander("View All Order Data"):
#             order_clean_df = pd.DataFrame(order_result, columns=["Name", "Items", "Qty", "ID"])
#             st.dataframe(order_clean_df)

#         st.subheader("Available Medicines")
#         drug_result = drug_view_all_data()

#         if len(drug_result) > 0:
#             # Get list of images sorted by modification time
#             image_folder = "images/"
#             image_files = [f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.png', '.jpeg', '.avif'))]
#             image_files.sort(key=lambda x: os.path.getmtime(os.path.join(image_folder, x)), reverse=False)

#             # Use the full list of medicines (no random sampling)
#             medicines_to_show = drug_result  # Use the full list instead of random.sample
#             num_images = min(len(image_files), len(medicines_to_show))

#             for i, drug in enumerate(medicines_to_show):
#                 st.subheader(drug[0])

#                 # Assign images to drugs in order
#                 if i < num_images:
#                     img_path = os.path.join(image_folder, image_files[i])
#                     try:
#                         img = Image.open(img_path)
#                         st.image(img, width=400, caption=f"Price: Rs. {drug[3]}")
#                     except Exception as e:
#                         st.warning(f"Failed to load image for {drug[0]}: {str(e)}")
#                 else:
#                     st.warning("No image available for this drug.")

#                 quantity_slider = st.slider(
#                     label=f"Select Quantity for {drug[0]}",
#                     min_value=0,
#                     max_value=int(drug[3]),
#                     key=f"slider_{drug[4]}"
#                 )
#                 st.info(f"When to Use: {drug[2]}")

#             if st.button("Buy Now"):
#                 selected_items = []
#                 for drug in medicines_to_show:
#                     quantity = st.session_state.get(f"slider_{drug[4]}", 0)
#                     if quantity > 0:
#                         selected_items.append((drug[0], quantity))

#                 if selected_items:
#                     O_items = ",".join([item[0] for item in selected_items])
#                     O_Qty = ",".join([str(item[1]) for item in selected_items])
#                     O_id = f"{username}#O{random.randint(0, 1000000)}"
#                     order_add_data(username, O_items, O_Qty, O_id)
#                     st.success("Order placed successfully!")
#                 else:
#                     st.warning("No items selected for purchase.")
#         else:
#             st.warning("No medicines available in the inventory.")

 
def customer(username, password):
    if getauthenicate(username, password):
        st.markdown(f"<div class='main-title'>Welcome {username}!</div>", unsafe_allow_html=True)
        
        st.title("Welcome to Pharmacy Store")
        st.subheader("Your Order Details")
        order_result = order_view_data(username)
        with st.expander("View All Order Data"):
            order_clean_df = pd.DataFrame(order_result, columns=["Name", "Items", "Qty", "ID"])
            st.dataframe(order_clean_df)

        st.subheader("Available Medicines")
        drug_result = drug_view_all_data()

        if len(drug_result) > 0:
            # Supported image formats
            image_extensions = ['.jpg', '.jpeg', '.png', '.avif']
            image_folder = "images/"

            # Iterate through all medicines in the database
            for drug in drug_result:
                drug_name = drug[0]  # Assuming drug name is the first column in the database
                st.subheader(drug_name)

                # Try to find the image file with supported extensions
                image_path = None
                for ext in image_extensions:
                    temp_path = os.path.join(image_folder, f"{drug_name}{ext}")
                    if os.path.exists(temp_path):
                        image_path = temp_path
                        break

                # Display the image if found
                if image_path:
                    try:
                        img = Image.open(image_path)
                        st.image(img, width=400, caption=f"Price: Rs. {drug[3]}")  # Assuming price is the 4th column
                    except Exception as e:
                        st.warning(f"Failed to load image for {drug_name}: {str(e)}")
                else:
                    st.warning(f"No image found for {drug_name} in supported formats: {', '.join(image_extensions)}")

                # Quantity slider for each drug
                quantity_slider = st.slider(
                    label=f"Select Quantity for {drug_name}",
                    min_value=0,
                    max_value=int(drug[3]),  # Assuming quantity is the 4th column
                    key=f"slider_{drug[4]}"  # Assuming drug ID is the 5th column
                )
                st.info(f"When to Use: {drug[2]}")  # Assuming usage is the 3rd column

            # Buy Now button
            if st.button("Buy Now"):
                selected_items = []
                for drug in drug_result:
                    quantity = st.session_state.get(f"slider_{drug[4]}", 0)  # Assuming drug ID is the 5th column
                    if quantity > 0:
                        selected_items.append((drug[0], quantity))  # Drug name and quantity

                if selected_items:
                    O_items = ",".join([item[0] for item in selected_items])
                    O_Qty = ",".join([str(item[1]) for item in selected_items])
                    O_id = f"{username}#O{random.randint(0, 1000000)}"
                    order_add_data(username, O_items, O_Qty, O_id)
                    
                    # Update drug quantities in the inventory
                    for drug_name, quantity_purchased in selected_items:
                        update_drug_quantity(drug_name, quantity_purchased)
                    
                    st.success("Order placed successfully!")
                else:
                    st.warning("No items selected for purchase.")
        else:
            st.warning("No medicines available in the inventory.") 
 
# def customer(username, password):
#     if getauthenicate(username, password):
#         st.markdown(f"<div class='main-title'>Welcome {username}!</div>", unsafe_allow_html=True)
        
#         st.title("Welcome to Pharmacy Store")
#         st.subheader("Your Order Details")
#         order_result = order_view_data(username)
#         with st.expander("View All Order Data"):
#             order_clean_df = pd.DataFrame(order_result, columns=["Name", "Items", "Qty", "ID"])
#             st.dataframe(order_clean_df)

#         st.subheader("Available Medicines")
#         drug_result = drug_view_all_data()

#         if len(drug_result) > 0:
#             # Get list of images sorted by modification time
#             image_folder = "images/"
#             image_files = [f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.png', '.jpeg', '.avif'))]
#             image_files.sort(key=lambda x: os.path.getmtime(os.path.join(image_folder, x)), reverse=False)

#             # Use the full list of medicines (no random sampling)
#             medicines_to_show = drug_result  # Use the full list instead of random.sample
#             num_images = min(len(image_files), len(medicines_to_show))

#             for i, drug in enumerate(medicines_to_show):
#                 st.subheader(drug[0])

#                 # Assign images to drugs in order
#                 if i < num_images:
#                     img_path = os.path.join(image_folder, image_files[i])
#                     try:
#                         img = Image.open(img_path)
#                         st.image(img, width=400, caption=f"Price: Rs. {drug[3]}")
#                     except Exception as e:
#                         st.warning(f"Failed to load image for {drug[0]}: {str(e)}")
#                 else:
#                     st.warning("No image available for this drug.")

#                 quantity_slider = st.slider(
#                     label=f"Select Quantity for {drug[0]}",
#                     min_value=0,
#                     max_value=int(drug[3]),
#                     key=f"slider_{drug[4]}"
#                 )
#                 st.info(f"When to Use: {drug[2]}")

#             if st.button("Buy Now"):
#                 selected_items = []
#                 for drug in medicines_to_show:
#                     quantity = st.session_state.get(f"slider_{drug[4]}", 0)
#                     if quantity > 0:
#                         selected_items.append((drug[0], quantity))

#                 if selected_items:
#                     O_items = ",".join([item[0] for item in selected_items])
#                     O_Qty = ",".join([str(item[1]) for item in selected_items])
#                     O_id = f"{username}#O{random.randint(0, 1000000)}"
#                     order_add_data(username, O_items, O_Qty, O_id)
                    
#                     # Update drug quantities in the inventory
#                     for drug_name, quantity_purchased in selected_items:
#                         update_drug_quantity(drug_name, quantity_purchased)
                    
#                     st.success("Order placed successfully!")
#                 else:
#                     st.warning("No items selected for purchase.")
#         else:
#             st.warning("No medicines available in the inventory.")
          
# Main Function
if __name__ == '__main__':
    drug_create_table()
    cust_create_table()
    order_create_table()

    # Decorate Side Panel
    st.sidebar.markdown(
        """
        <div class="sidebar-title"><h2>Pharmacy Management System</h2></div>
        <br>
        <div class="sidebar-text">
            Welcome to the Pharmacy Management System! This system allows you to manage drugs, customers, and orders efficiently.
        </div>
        <br>
        """,
        unsafe_allow_html=True,
    )

    menu = ["Login", "SignUp", "Admin"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        st.markdown('<div class="main-title">Pharmacy Management System</div>', unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("**Login to access your account and manage your orders.**")
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        if st.sidebar.checkbox(label="Login"):
            customer(username, password)

    elif choice == "SignUp":
        st.markdown('<div class="main-title">Pharmacy Management System</div>', unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("**Create a new account to start using the Pharmacy Management System.**")
        cust_name = st.text_input("Name")
        cust_password = st.text_input("Password", type='password', key=1000)
        cust_password1 = st.text_input("Confirm Password", type='password', key=1001)
        col1, col2, col3 = st.columns(3)
        with col1:
            cust_email = st.text_area("Email ID", placeholder="Enter your email")
        with col2:
            cust_area = st.text_area("State", placeholder="Enter your state")
        with col3:
            cust_number = st.text_area("Phone Number", placeholder="Enter your phone number")
        if st.button("Signup"):
            if cust_password == cust_password1:
                customer_add_data(cust_name, cust_password, cust_email, cust_area, cust_number)
                st.success("Account Created Successfully!")
                st.info("Go to the Login Menu to log in")
            else:
                st.warning('Passwords do not match. Please try again.')

    elif choice == "Admin":
        st.markdown('<div class="main-title">Pharmacy Management System</div>', unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("**Admin Dashboard**")
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        if username == 'admin' and password == 'admin':
            admin()

    # Footer
    st.markdown(
        """
        <div class="footer">
            Pharmacy Management System<br>
            Developed by Laxman<br>
        </div>
        """,
        unsafe_allow_html=True,
    )
