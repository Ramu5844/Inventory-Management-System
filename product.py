from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from employee import connect_database
import mysql.connector

def connect_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database="inventorysystem"   # you can set the DB here
        )
        cursor = connection.cursor()
        return cursor, connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None, None

def select_data(event, Category_combobox, Supplier_combobox, name_entry, price_entry, quantity_entry, Status_combobox, treeview):
    selected_item = treeview.focus()
    if not selected_item:
        return
    content = treeview.item(selected_item, "values")
    if not content:
        return
    Category_combobox.set(content[1])   # category
    Supplier_combobox.set(content[2])   # supplier
    name_entry.delete(0, "end")
    name_entry.insert(0, content[3])
    price_entry.delete(0, "end")
    price_entry.insert(0, content[4])
    quantity_entry.delete(0, "end")
    quantity_entry.insert(0, content[5])
    Status_combobox.set(content[6])

def treeview_data(treeview):
    cursor, connection = connect_database()   # make sure order matches
    if not cursor or not connection:
        return

    cursor.execute("SELECT * FROM product_data")
    rows = cursor.fetchall()

    # clear existing rows
    for item in treeview.get_children():
        treeview.delete(item)

    # insert new rows
    for row in rows:
        treeview.insert("", "end", values=row)

    cursor.close()
    connection.close()

def fetch_supplier_category(Category_combobox, Supplier_combobox):
    category_option = []
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    
    cursor.execute('SELECT name FROM category_data')
    names = cursor.fetchall()
    for name in names:
        category_option.append(name[0])
    Category_combobox.config(values=category_option)

    supplier_option = []
    cursor.execute('SELECT name FROM supplier_data')
    suppliers = cursor.fetchall()
    for supplier in suppliers:
        supplier_option.append(supplier[0])
    Supplier_combobox.config(values=supplier_option)

    cursor.close()
    connection.close()
        
def add_product(category, supplier, name, price, quantity, status, treeview):
    if category == 'Empty':
        messagebox.showerror('Error', 'Please add categories')
    elif supplier == 'Empty':
        messagebox.showerror('Error', 'Please add supplier')
    elif category == 'Select' or supplier == 'Select' or name == '' or price == '' or quantity == '' or status == 'Select Status':
        messagebox.showerror('Error', 'All fields are required')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        # Use the correct database
        cursor.execute('USE inventorysystem')
        # Fix typo: varchar not varachar
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS product_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                category VARCHAR(100),
                supplier VARCHAR(100),
                name VARCHAR(100),
                price DECIMAL(10,2),
                quantity INT,
                status VARCHAR(50)
            )''')
        cursor.execute('SELECT * from product_data WHERE category=%s AND supplier=%s AND name=%s',(category,supplier,name))
        existing_product=cursor.fetchone()
        if existing_product:
            messagebox.showerror('Error','Product already exist')
            return
        cursor.execute(
            'INSERT INTO product_data(category,supplier,name,price,quantity,status) VALUES (%s,%s,%s,%s,%s,%s)',
            (category, supplier, name, price, quantity, status)
        )
        connection.commit()
        messagebox.showinfo('Success', 'Data is inserted')
        treeview_data(treeview)
        cursor.close()
        connection.close()

def update_product(category, supplier, name, price, quantity, status, treeview):
    selected_items = treeview.selection()
    if not selected_items:
        messagebox.showerror('Error', 'Select a row first')
        return
    item_id = selected_items[0]
    content = treeview.item(item_id, "values")
    id = content[0]  # assuming first column is product id
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('USE inventorysystem')
        cursor.execute('SELECT * FROM product_data WHERE id=%s', (id,))
        current_data = cursor.fetchone()
        current_data = current_data[1:]  # skip id

        new_data = (category, supplier, name, price, quantity, status)

        if current_data == new_data:
            messagebox.showinfo('Info', 'No change detected')
            return
        cursor.execute(
            "UPDATE product_data SET category=%s, supplier=%s, name=%s, price=%s, quantity=%s, status=%s WHERE id=%s",
            (category, supplier, name, price, quantity, status, id)
        )
        connection.commit()
        treeview_data(treeview)
        messagebox.showinfo('Success', 'Product updated')
    except Exception as e:
        messagebox.showerror('Error', f'{e}')
    finally:
        cursor.close()
        connection.close()

def delete_product(treeview):
    selected_items = treeview.selection()
    if not selected_items:
        messagebox.showerror("Error", "Please select a product to delete")
        return
    item_id = selected_items[0]
    values = treeview.item(item_id, "values")
    product_id = values[0]  # assuming first column is id
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute("USE inventorysystem")
        cursor.execute("DELETE FROM product_data WHERE id=%s", (product_id,))
        connection.commit()
        treeview.delete(item_id)  # remove from UI
        messagebox.showinfo("Success", "Product deleted")
    except Exception as e:
        messagebox.showerror("Error", f"{e}")
    finally:
        cursor.close()
        connection.close()
        
def clear(category_combobox, supplier_combobox, name_entry, price_entry, quantity_entry, status_combobox, treeview):
    category_combobox.set("Select")
    supplier_combobox.set("Select")
    status_combobox.set("Select Status")
    name_entry.delete(0, "end")
    price_entry.delete(0, "end")
    quantity_entry.delete(0, "end")
    
    for item in treeview.selection():
        treeview.selection_remove(item)
        
def search_product(search_combobox, search_entry, treeview):
    keyword = search_entry.get()
    if keyword == '':
        messagebox.showerror('Error', 'Enter a search term')
        return
    cursor, connection = connect_database()   # ✅ cursor first
    if not cursor or not connection:
        return
    try:
        cursor.execute("USE inventorysystem")
        cursor.execute("SELECT * FROM supplier_data WHERE name=%s", (keyword,))
        record = cursor.fetchone()
        
        treeview.delete(*treeview.get_children())
        if record:
            treeview.insert('', 'end', values=record)
        else:
            messagebox.showinfo('Info', 'No record found')
    except Exception as e:
        messagebox.showerror("Error", f"{e}")
    finally:
        cursor.close()
        connection.close()
    
def show_all(treeview, search_entry):
    treeview_data(treeview)
    search_entry.delete(0, END)
     
def product_form(window):
    global back_image
    product_frame=Frame(window,width=1070, height=567, bg='white')
    product_frame.place(x=200, y=100)
      
    back_image = PhotoImage(file='back.png')
    back_button=Button(product_frame,image=back_image, bd=0, cursor='hand2', bg='white',
                       command=lambda: product_frame.place_forget())
    back_button.place(x=10, y=30)
    
    left_frame = Frame(product_frame,bg='white',bd=2,relief=RIDGE)
    left_frame.place(x=10,y=65)
    
    heading_label= Label(left_frame, text='Manage Product Details', font=('times new roman',14 ,'bold'),
                         bg='#0f4d7d', fg='white')
    heading_label.grid(row=0, columnspan=2,sticky='we')
    
    
    Category_label=Label(left_frame,text='Category',font=('times new roman',14,'bold'),bg='white')
    Category_label.grid(row=1,column=0,padx=20,sticky='w')
    Category_combobox=ttk.Combobox(left_frame,font=('times new roman',14),width=18,state='readonly')
    Category_combobox.grid(row=1,column=1,pady=15)
    Category_combobox.set('Select') 
    
    Supplier_label=Label(left_frame,text='Supplier',font=('times new roman',14,'bold'),bg='white')
    Supplier_label.grid(row=2,column=0,padx=20,sticky='w')
    Supplier_combobox=ttk.Combobox(left_frame,font=('times new roman',14),width=18,state='readonly')
    Supplier_combobox.grid(row=2,column=1,pady=15)
    Supplier_combobox.set('Select')
        
    name_label=Label(left_frame,text='Name',font=('times new roman',14,'bold'),bg='lightyellow')
    name_label.grid(row=3,column=0,padx=20,sticky='w')
    name_entry=Entry(left_frame,font=('times new roman',14,'bold'),bg='lightyellow')
    name_entry.grid(row=3,column=1,pady=25)
           
    price_label=Label(left_frame,text='Price',font=('times new roman',14,'bold'),bg='lightyellow')
    price_label.grid(row=4,column=0,padx=20,sticky='w')
    price_entry=Entry(left_frame,font=('times new roman',14,'bold'),bg='lightyellow')
    price_entry.grid(row=4,column=1,pady=25)
    
       
    quantity_label=Label(left_frame,text='Quantity',font=('times new roman',14,'bold'),bg='lightyellow')
    quantity_label.grid(row=5,column=0,padx=20,sticky='w')
    quantity_entry=Entry(left_frame,font=('times new roman',14,'bold'),bg='lightyellow')
    quantity_entry.grid(row=5,column=1,pady=25)    

    Status_label=Label(left_frame,text='Status',font=('times new roman',14,'bold'),bg='white')
    Status_label.grid(row=6,column=0,padx=20,sticky='w')
    Status_combobox=ttk.Combobox(left_frame,values=('Active','InActive'),font=('times new roman',14),width=18,state='readonly')
    Status_combobox.grid(row=6,column=1,pady=15)
    Status_combobox.set('Select Status')
    
    button_frame=Frame(left_frame,bg='white')
    button_frame.grid(row=7,columnspan=2,pady=15)
    
    add_button = Button(
    button_frame,
    text='Add',
    font=('times new roman', 14),
    width=8,
    cursor='hand2',
    fg='white',
    bg="#0f4d7d",
    command=lambda: add_product(
        Category_combobox.get(),
        Supplier_combobox.get(),
        name_entry.get(),
        price_entry.get(),
        quantity_entry.get(),
        Status_combobox.get(),
        treeview
    )
)

    add_button.grid(row=0, column=0, padx=20)
    
    update_button =Button(button_frame,text='Update',font=('times new roman',14),width=8,cursor='hand2',
                       fg='white',bg="#0f4d7d",command=lambda: update_product(
        Category_combobox.get(),
        Supplier_combobox.get(),
        name_entry.get(),
        price_entry.get(),
        quantity_entry.get(),
        Status_combobox.get(),
        treeview
    ))
    
    update_button.grid(row=0, column=1, padx=20)
    
    delete_button = Button(
    button_frame,
    text='Delete',
    font=('times new roman', 14),
    width=8,
    cursor='hand2',
    fg='white',
    bg="#0f4d7d",
    command=lambda: delete_product(treeview)   # ✅ only pass treeview
)

    
    delete_button.grid(row=0, column=2, padx=20)

    clear_button = Button(
    button_frame,
    text='Clear',
    font=('times new roman', 14),
    width=8,
    cursor='hand2',
    fg='white',
    bg="#0f4d7d",
    command=lambda: clear(
        Category_combobox,
        Supplier_combobox,
        name_entry,
        price_entry,
        quantity_entry,
        Status_combobox,
        treeview
    )
)
    clear_button.grid(row=0, column=3, padx=20)
     
    search_frame = LabelFrame(
    product_frame,
    text='Search Product',
    font=('times new roman', 14, 'bold'),
    bg='white',
    bd=2,
    relief=RIDGE
)
    search_frame.place(x=540, y=40,)

    search_combobox = ttk.Combobox(
        search_frame,
        values=('Category', 'Supplier', 'Name', 'Status'),
        state='readonly',
        width=12,
        font=('times new roman', 14)
    )
    search_combobox.grid(row=0, column=0, padx=8, pady=12)
    search_combobox.set('Search By')

    search_entry = Entry(
        search_frame,
        font=('times new roman', 14, 'bold'),
        bg='lightyellow',
        width=14
    )
    search_entry.grid(row=0, column=1, padx=8)

    search_button = Button(
        search_frame,
        text='Search',
        font=('times new roman', 14),
        width=8,
        cursor='hand2',
        fg='white',
        bg='#010c48',command=lambda:search_product(search_combobox,search_entry,treeview)
    )
    search_button.grid(row=0, column=2, padx=8)

    show_button = Button(
        search_frame,
        text='Show All',
        font=('times new roman', 14),
        width=8,
        cursor='hand2',
        fg='white',
        bg='#010c48',command=lambda: show_all(treeview,search_entry)
    )
    show_button.grid(row=0, column=3, padx=8)
    
    
    
    treeview_frame=Frame(product_frame)
    treeview_frame.place(x=540, y=125, width=520, height=430)
    
    
    scrolly=Scrollbar(treeview_frame,orient=VERTICAL)
    scrollx=Scrollbar(treeview_frame,orient=HORIZONTAL)
    
    treeview=ttk.Treeview(treeview_frame,column=('id','category','supplier','name','price','quantity','status'),show='headings',
                          yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
    
    scrolly.pack(side=RIGHT,fill=Y)
    scrollx.pack(side=BOTTOM,fill=X)
    scrollx.config(command=treeview.xview)
    scrolly.config(command=treeview.yview)  
    treeview.pack(fill=BOTH,expand=1)
    
    treeview.heading('id',text='Id')
    treeview.heading('category',text='Category')
    treeview.heading('supplier',text='Supplier')
    treeview.heading('name',text='Name')  
    treeview.heading('price',text='Price')
    treeview.heading('quantity',text='Quantity')
    treeview.heading('status',text='Status')
    
    fetch_supplier_category(Category_combobox,Supplier_combobox)
    
    treeview_data(treeview)
    
    treeview_data(treeview)
    treeview.bind('<ButtonRelease -1>',lambda event:select_data(event,Category_combobox,Supplier_combobox,name_entry,price_entry,quantity_entry,Status_combobox,treeview))
    return product_frame
