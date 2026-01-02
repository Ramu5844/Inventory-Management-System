from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from employee import connect_database

from tkinter import *
from tkinter import ttk, messagebox
from employee import connect_database

def add_supplier(invoice, name, contact, description, treeview):
    if invoice == '' or name == '' or contact == '' or description.strip() == '':
        messagebox.showerror('Error', 'All fields are required')
        return

    connection, cursor = connect_database()
    if not connection:
        return

    try:
        cursor.execute(
            "INSERT INTO supplier_data VALUES (%s,%s,%s,%s)",
            (invoice, name, contact, description.strip())
        )
        connection.commit()
        treeview_data(treeview)
        messagebox.showinfo('Success', 'Supplier added successfully')
    except Exception as e:
        messagebox.showerror('Error', f'{e}')
    finally:
        cursor.close()
        connection.close()


# ---------------- SHOW ALL ----------------
def treeview_data(treeview):
    connection, cursor = connect_database()
    if not connection:
        return

    cursor.execute("SELECT * FROM supplier_data")
    records = cursor.fetchall()

    treeview.delete(*treeview.get_children())
    for record in records:
        treeview.insert('', END, values=record)

    cursor.close()
    connection.close()

def select_data(event, invoice_entry, name_entry, contact_entry, description_text, treeview):
    selected = treeview.selection()
    if not selected:
        return

    values = treeview.item(selected)['values']

    invoice_entry.delete(0, END)
    name_entry.delete(0, END)
    contact_entry.delete(0, END)
    description_text.delete(1.0, END)

    invoice_entry.insert(0, values[0])
    name_entry.insert(0, values[1])
    contact_entry.insert(0, values[2])
    description_text.insert(1.0, values[3])
    
def update_supplier(invoice, name, contact, description, treeview):
    if not treeview.selection():
        messagebox.showerror('Error', 'Select a row first')
        return

    connection, cursor = connect_database()
    if not connection:
        return

    try:
        cursor.execute(
            "UPDATE supplier_data SET name=%s, contact=%s, description=%s WHERE invoice=%s",
            (name, contact, description.strip(), invoice)
        )
        connection.commit()
        treeview_data(treeview)
        messagebox.showinfo('Success', 'Supplier updated')
    except Exception as e:
        messagebox.showerror('Error', f'{e}')
    finally:
        cursor.close()
        connection.close()
        
def delete_supplier(invoice, treeview):
    if not treeview.selection():
        messagebox.showerror('Error', 'Select a row first')
        return

    if not messagebox.askyesno('Confirm', 'Delete this record?'):
        return

    connection, cursor = connect_database()
    if not connection:
        return

    try:
        cursor.execute(
            "DELETE FROM supplier_data WHERE invoice=%s",
            (invoice,)
        )
        connection.commit()
        treeview_data(treeview)
        messagebox.showinfo('Success', 'Supplier deleted')
    except Exception as e:
        messagebox.showerror('Error', f'{e}')
    finally:
        cursor.close()
        connection.close()


def search_supplier(invoice, treeview):
    if invoice == '':
        messagebox.showerror('Error', 'Enter invoice number')
        return

    connection, cursor = connect_database()
    if not connection:
        return

    cursor.execute(
        "SELECT * FROM supplier_data WHERE invoice=%s",
        (invoice,)
    )
    record = cursor.fetchone()

    treeview.delete(*treeview.get_children())
    if record:
        treeview.insert('', END, values=record)
    else:
        messagebox.showinfo('Info', 'No record found')

    cursor.close()
    connection.close()
    
def show_all(treeview, search_entry):
    treeview_data(treeview)
    search_entry.delete(0, END)

def clear(invoice_entry, name_entry, contact_entry, description_text, treeview):
    invoice_entry.delete(0, END)
    name_entry.delete(0, END)
    contact_entry.delete(0, END)
    description_text.delete(1.0, END)
    treeview.selection_remove(treeview.selection())

def supplier_form(window):
    global back_image
    supplier_frame=Frame(window,width=1070,height=567,background='white')
    supplier_frame.place(x=200, y=100)
    
    heading_label= Label(supplier_frame, text='Manage Supplier Details', font=('times new roman',16 ,'bold'),
                         bg='#0f4d7d', fg='white')
    heading_label.place(x=0, y=0, relwidth=1)
    
    back_image = PhotoImage(file='back.png')
    back_button=Button(supplier_frame,image=back_image, bd=0, cursor='hand2', bg='white',
                       command=lambda: supplier_frame.place_forget())
    back_button.place(x=10, y=30)
    
    left_frame = Frame(supplier_frame,bg='white')
    left_frame.place(x=10,y=100)
    
    invoice_label=Label(left_frame,text='Invoice No',font=('times new roman',14,'bold'),bg='white')
    invoice_label.grid(row=0,column=0,padx=20)
    invoice_entry=Entry(left_frame,font=('times new roman',14,'bold'),bg='lightyellow')
    invoice_entry.grid(row=0,column=1)
    
    name_label=Label(left_frame,text='Supplier Name',font=('times new roman',14,'bold'),bg='white')
    name_label.grid(row=1,column=0,padx=20,pady='25')
    name_entry=Entry(left_frame,font=('times new roman',14,'bold'),bg='lightyellow')
    name_entry.grid(row=1,column=1)
    
    contact_label=Label(left_frame,text='Contact',font=('times new roman',14,'bold'),bg='white')
    contact_label.grid(row=2,column=0,padx=20)
    contact_entry=Entry(left_frame,font=('times new roman',14,'bold'),bg='lightyellow')
    contact_entry.grid(row=2,column=1)
    
    description_label= Label(left_frame, text='Description', font=('times new roman',14,'bold'),bg='white')
    description_label.grid(row=3, column=0,padx=(20,40),sticky='nw',pady=25) 
    description_text=Text(left_frame,width=25,height=6,bd=2,bg='lightyellow')
    description_text.grid(row=3,column=1,pady=25)  
    
    button_frame=Frame(left_frame,bg='white')
    button_frame.grid(row=4,columnspan=2)
    
    add_button =Button(button_frame,text='Add',font=('times new roman',14),width=8,cursor='hand2',
                       fg='white',bg="#0f4d7d",command=lambda:add_supplier(invoice_entry.get(),contact_entry.get(),name_entry.get(),description_text.get(1.0,END),treeview))
    
    add_button.grid(row=0, column=0, padx=20)
    
    
    update_button = Button(button_frame,text='Update',font=('times new roman',14),width=8, cursor='hand2',
                           fg='white',bg='#0f4d7d',command=lambda:update_supplier(invoice_entry.get(),name_entry.get(),contact_entry.get(),description_text.get(1.0,END).strip(),treeview))
    update_button.grid(row=0, column=1)
    
    
    delete_button =Button(button_frame,text='Delete',font=('times new roman',14),width=8,cursor='hand2',
                       fg='white',bg='#0f4d7d',command=lambda: delete_supplier(invoice_entry.get(),treeview))
    delete_button.grid(row=0, column=2,padx=20)
    
    
    clear_button =Button(button_frame,text='Clear',font=('times new roman',14),width=8,cursor='hand2',
                       fg='white',bg='#0f4d7d',command=lambda: clear(invoice_entry,name_entry,contact_entry,description_text,treeview))
    clear_button.grid(row=0, column=3)
    
    right_frame=Frame(supplier_frame,bg='white')
    right_frame.place(x=520,y=90,width=500,height=350)
    
    search_frame=Frame(right_frame,bg='white')
    search_frame.pack()
     
    num_label = Label(search_frame, text='Invoice No',font=('times new roman',14,'bold'),bg='white')
    num_label.grid(row=0, column=0,padx=(0,10),sticky='w')
    search_entry=Entry(search_frame,font=('times new roman',14,'bold'),bg='lightyellow',width=12)
    search_entry.grid(row=0,column=1)
    
     
    search_button =Button(search_frame,text='Search',font=('times new roman',14),width=8,cursor='hand2',
                       fg='white',bg='#0f4d7d',command=lambda:search_supplier(search_entry.get(),treeview))
    search_button.grid(row=0, column=2,padx=15)
    
    show_button =Button(search_frame,text='Show All ',font=('times new roman',14),width=8,cursor='hand2',
                       fg='white',bg='#0f4d7d',command=lambda: show_all(treeview,search_entry))
    show_button.grid(row=0, column=3)
    
    scrolly=Scrollbar(right_frame,orient=VERTICAL)
    scrollx=Scrollbar(right_frame,orient=HORIZONTAL)
    
    treeview=ttk.Treeview(right_frame,column=('invoice','name','contact','description'),show='headings',
                          yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
    
    scrolly.pack(side=RIGHT,fill=Y)
    scrollx.pack(side=BOTTOM,fill=X)
    scrollx.config(command=treeview.xview)
    scrolly.config(command=treeview.yview)  
    treeview.pack(fill=BOTH,expand=1)
    
    treeview.pack()
    treeview.heading('invoice',text='Invoice Id')
    treeview.heading('name',text='Supplier Name')
    treeview.heading('contact',text='Contact')
    treeview.heading('description',text='Description')
    
    treeview.column('invoice',width=80)
    treeview.column('name',width=160)
    treeview.column('contact',width=120)
    treeview.column('description',width=300)
    
    treeview_data(treeview)
    treeview.bind('<ButtonRelease -1>',lambda event:select_data(event,invoice_entry,name_entry,contact_entry,description_text,treeview))
    return supplier_frame