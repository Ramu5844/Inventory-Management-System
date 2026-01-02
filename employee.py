from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import messagebox
import pymysql

def connect_database():
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='12345',
            database='inventorysystem'
        )
        cursor = connection.cursor()
        return connection, cursor

    except Exception as e:
        messagebox.showerror(
            'Error',
            f'Database connectivity issue\n{e}'
        )
        return None, None

connect_database()

def create_database_table():
    connection, cursor = connect_database()
    if not connection:
        return
    
    cursor.execute('CREATE DATABASE IF NOT EXISTS inventorysystem')
    cursor.execute('USE inventorysystem')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees_data(
            empid INT PRIMARY KEY,
            name VARCHAR(225),
            email VARCHAR(225),
            gender VARCHAR(100),
            dob VARCHAR(100),
            contact VARCHAR(225),
            employment_type VARCHAR(225),
            education VARCHAR(225),
            work_shift VARCHAR(225),
            address VARCHAR(224),
            doj VARCHAR(20),
            salary VARCHAR(100),
            usertype VARCHAR(50),
            password VARCHAR(225)
        )
    ''')

    connection.commit()
    cursor.close()
    connection.close()

def treeview_data():
    connection, cursor = connect_database()
    if not connection:
        return
    try:
        cursor.execute("SELECT * FROM employees_data")
        records = cursor.fetchall()

        employee_treeview.delete(*employee_treeview.get_children())
        for row in records:
            employee_treeview.insert('', END, values=row)

    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')

    finally:
        cursor.close()
        connection.close()      
        
def select_data(event, empid_entry, name_entry, email_entry,
                gender_combobox, dob_date_entry, contact_entry,
                Employment_combobox, Education_combobox,
                Work_combobox, address_text, doj_date_entry,
                salary_entry, User_combobox, password_entry):

    index = employee_treeview.selection()
    if not index:
        return

    content = employee_treeview.item(index)
    row = content['values']
    clear_fields(
        empid_entry, name_entry, email_entry,
        gender_combobox, dob_date_entry, contact_entry,
        Employment_combobox, Education_combobox,
        Work_combobox, address_text, doj_date_entry,
        salary_entry, User_combobox, password_entry
    )

    empid_entry.insert(0, row[0])
    name_entry.insert(0, row[1])
    email_entry.insert(0, row[2])
    gender_combobox.set(row[3])
    dob_date_entry.set_date(row[4])
    contact_entry.insert(0, row[5])
    Employment_combobox.set(row[6])
    Education_combobox.set(row[7])
    Work_combobox.set(row[8])
    address_text.insert('1.0', row[9])
    doj_date_entry.set_date(row[10])
    salary_entry.insert(0, row[11])
    User_combobox.set(row[12])
    password_entry.insert(0, row[13])
       
def add_employee(empid, name, email, gender, dob, contact,
                 employment_type, education, work_shift,
                 address, doj, salary, usertype, password):
    if empid == '' or name == '' or email == '':
        messagebox.showerror('Error', 'All fields are required')
        return

    connection, cursor = connect_database()
    if not connection:
       return
    try:
        cursor.execute("""
            INSERT INTO employees_data
            (empid, name, email, gender, dob, contact,
             employment_type, education, work_shift,
             address, doj, salary, usertype, password)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            empid, name, email, gender, dob, contact,
            employment_type, education, work_shift,
            address, doj, salary, usertype, password
        ))

        connection.commit()
        messagebox.showinfo('Success', 'Employee added successfully')

    except Exception as e:
        messagebox.showerror('Database Error', str(e))

    finally:
        cursor.close()
        connection.close()

def clear_fields(empid_entry,name_entry,email_entry,gender_combobox,dob_date_entry,contact_entry,Employment_combobox,
                 Education_combobox,Work_combobox,address_text,doj_date_entry,salary_entry,User_combobox,password_entry):
    empid_entry.delete(0, END)
    name_entry.delete(0, END)
    email_entry.delete(0, END)
    from  datetime import date
    
    gender_combobox.set('Select Gender')    
    dob_date_entry.set_date(date.today())
    contact_entry.delete(0, END)
    Employment_combobox.set('Select')
    Education_combobox.set('Select')
    Work_combobox.set('Select')

    address_text.delete(1.0, END)
    doj_date_entry.set_date(date.today())

    salary_entry.delete(0, END)
    User_combobox.set('Select User Type')
    password_entry.delete(0, END)
       
def update_employee(empid, name, email, gender, dob, contact,
                    employment_type, education, work_shift,
                    address, doj, salary, user_type, password):

    selected = employee_treeview.selection()
    if not selected:
        messagebox.showerror('Error', 'No row is selected')
        return
    # ✅ CORRECT ORDER
    connection, cursor = connect_database()
    if not connection:
        return
    try:
        # 🔹 Check existing record
        cursor.execute(
            "SELECT name, email, gender, dob, contact, employment_type, "
            "education, work_shift, address, doj, salary, usertype, password "
            "FROM employees_data WHERE empid=%s",
            (empid,)
        )

        current_data = cursor.fetchone()
        if not current_data:
            messagebox.showerror('Error', 'Employee not found')
            return

        address = address.strip()

        new_data = (
            name, email, gender, dob, contact,
            employment_type, education, work_shift,
            address, doj, salary, user_type, password
        )

        if current_data == new_data:
            messagebox.showinfo('Info', 'No changes detected')
            return

        # 🔹 UPDATE QUERY
        cursor.execute("""
            UPDATE employees_data SET
                name=%s,
                email=%s,
                gender=%s,
                dob=%s,
                contact=%s,
                employment_type=%s,
                education=%s,
                work_shift=%s,
                address=%s,
                doj=%s,
                salary=%s,
                usertype=%s,
                password=%s
            WHERE empid=%s
        """, (
            name, email, gender, dob, contact,
            employment_type, education, work_shift,
            address, doj, salary, user_type, password, empid
        ))
        connection.commit()
        treeview_data()
        messagebox.showinfo('Success', 'Employee updated successfully')

    except Exception as e:
        messagebox.showerror('Database Error', str(e))
    finally:
        cursor.close()
        connection.close()

def delete_employee(empid):
    selected = employee_treeview.selection()
    if not selected:
        messagebox.showerror('Error', 'No row is selected')
        return
    confirm = messagebox.askyesno(
        'Confirm',
        'Do you really want to delete this employee?'
    )
    if not confirm:
        return
    connection, cursor = connect_database()
    if not connection:
        return
    try:
        cursor.execute(
            "DELETE FROM employees_data WHERE empid=%s",
            (empid,)
        )
        connection.commit()

        treeview_data()
        messagebox.showinfo('Success', 'Employee deleted successfully')
    except Exception as e:
        messagebox.showerror('Database Error', str(e))
    finally:
        cursor.close()
        connection.close()
                
def search_employee(search_option, value):
    if search_option == 'Search By':
        messagebox.showerror('Error', 'No option selected')
        return

    if value.strip() == '':
        messagebox.showerror('Error', 'Enter value to search')
        return
    column_map = {
        'Employee ID': 'empid',
        'Name': 'name',
        'Email': 'email',
        'Contact': 'contact',
        'User Type': 'usertype'
    }

    if search_option not in column_map:
        messagebox.showerror('Error', 'Invalid search option')
        return

    column = column_map[search_option]

    connection, cursor = connect_database()
    if not connection:
        return
    try:
        query = f"SELECT * FROM employees_data WHERE {column} LIKE %s"
        cursor.execute(query, (value + '%',))
        records = cursor.fetchall()
        employee_treeview.delete(*employee_treeview.get_children())

        if not records:
            messagebox.showinfo('Info', 'No record found')
            return
        for record in records:
            employee_treeview.insert('', END, values=record)

    except Exception as e:
        messagebox.showerror('Database Error', str(e))
    finally:
        cursor.close()
        connection.close()
            
def show_all(search_entry,search_combobox):
    treeview_data()
    search_entry.delete(0,END)
    search_combobox.set('Search By')             

def employee_form(window):
    for widget in window.winfo_children():
        if str(widget) == ".!frame2": 
            continue

    global back_image, employee_frame,employee_treeview
    employee_frame = Frame(window, width=1070, height=567, bg="white", bd=3, relief=RIDGE)
    employee_frame.place(x=200, y=100)

    headingLabel = Label(employee_frame,text='Manage Employee Details',font=('times new roman', 16, 'bold'),bg='#0f4d7d',fg='white')
    headingLabel.place(x=0, y=0, relwidth=1)
    
    back_image = PhotoImage(file="back.png")    
    
    top_frame =Frame(employee_frame,bg ='white') #bg ='white'
    top_frame.place(x=0,y=40,relwidth=1,height=235)
    
    back_button = Button(employee_frame,image=back_image,bd=0,cursor="hand2",bg="white",command=lambda: employee_frame.place_forget())
    back_button.place(x=10, y=30)
    employee_frame.back_image = back_image
    
    serach_frame =Frame(top_frame,bg='white')
    serach_frame.pack()
    search_combobox=ttk.Combobox(serach_frame,values=('EmpId','Name','Email'),font=('times new roman',12),state='readonly')
    search_combobox.set('Search By')
    search_combobox.grid(row=0,column=0,padx=20)
    search_entry=Entry(serach_frame,font=('times new roman',12),bg='lightyellow')
    search_entry.grid(row=0,column=1)
    search_button=Button(serach_frame,text='Search',font=('times new roman',12),width=10,cursor='hand2',
                         fg='white',bg='#010c48',command=lambda:search_employee(search_combobox.get(),search_entry.get()))
    search_button.grid(row=0,column=2,padx=20)
    show_button=Button(serach_frame,text='Show All',font=('times new roman',12),width=10,cursor='hand2',
                       fg='white',bg='#010c48',command=lambda:show_all(search_entry,search_combobox))
    show_button.grid(row=0,column=3,padx=20)
    
    horizontal_scrollbar=Scrollbar(top_frame,orient=HORIZONTAL)
    vertical_scrollbar=Scrollbar(top_frame,orient=VERTICAL)
    
    employee_treeview = ttk.Treeview(top_frame,
    columns=('empid','name','email','gender','contact','dob','employment_type',
             'education','work_shift','address','doj','salary','usertype'),
    show='headings',yscrollcommand=vertical_scrollbar.set,xscrollcommand=horizontal_scrollbar.set)
    
    horizontal_scrollbar.pack(side=BOTTOM,fill=X)
    vertical_scrollbar.pack(side=RIGHT,fill=Y,pady=(10,0))
    horizontal_scrollbar.config(command=employee_treeview.xview)
    vertical_scrollbar.config(command=employee_treeview.xview)
        
    employee_treeview.pack(pady=(10,0)) 
    
    employee_treeview.heading('empid',text='Empid')
    employee_treeview.heading('name',text='Name') 
    employee_treeview.heading('email',text='Email') 
    employee_treeview.heading('gender',text='Gender')
    employee_treeview.heading('contact',text='Contact')
    employee_treeview.heading('dob',text='Data of Birth')
    employee_treeview.heading('employment_type',text='Employment Type') 
    employee_treeview.heading('education',text='Education')
    employee_treeview.heading('work_shift',text='Work Shift')
    employee_treeview.heading('address',text='Address')
    employee_treeview.heading('doj',text='Date of Joining')
    employee_treeview.heading('salary',text='Salary')
    employee_treeview.heading('usertype',text='User Type') 
        
    employee_treeview.column('empid', width=60)
    employee_treeview.column('name', width=140)
    employee_treeview.column('email', width=180)
    employee_treeview.column('gender', width=80)
    employee_treeview.column('dob', width=100)
    employee_treeview.column('employment_type', width=120)
    employee_treeview.column('education', width=120)
    employee_treeview.column('work_shift', width=100)
    employee_treeview.column('address', width=200)
    employee_treeview.column('doj', width=100)
    employee_treeview.column('salary', width=140)
    employee_treeview.column('usertype', width=120)
    
    treeview_data()
    
    detail_frame=Frame(employee_frame,bg='white')
    detail_frame.place(x=20,y=280)
    
    empid_label=Label(detail_frame,text='Empid',font=('times new roman',12),bg='white')
    empid_label.grid(row=0,column=0,padx=20,pady=10,sticky='w')
    empid_entry=Entry(detail_frame,font=('times new roman',12),bg='lightyellow')
    empid_entry.grid(row=0,column=1,padx=20,pady=10)
    
    name_label=Label(detail_frame,text='Name',font=('times new roman',12),bg='white')
    name_label.grid(row=0,column=2,padx=20,pady=10,sticky='w')
    name_entry=Entry(detail_frame,font=('times new roman',12),bg='lightyellow')
    name_entry.grid(row=0,column=3,padx=20,pady=10)
    
    email_label=Label(detail_frame,text='Email',font=('times new roman',12),bg='white')
    email_label.grid(row=0,column=4,padx=20,pady=10,sticky='w')
    email_entry=Entry(detail_frame,font=('times new roman',12),bg='lightyellow')
    email_entry.grid(row=0,column=5,padx=20,pady=10)
    
    gender_label=Label(detail_frame,text='Gender',font=('times new roman',12),bg='white')
    gender_label.grid(row=1,column=0,padx=20,pady=10,sticky='w')
    
    gender_combobox=ttk.Combobox(detail_frame,values=('Male','Female'),font=('times new roman',12),width=18,state='readonly')
    gender_combobox.set('Select Gender')
    gender_combobox.grid(row=1,column=1)
    
    dob_label=Label(detail_frame,text='Date of Birth',font=('times new roman',12),bg='white')
    dob_label.grid(row=1,column=2,padx=20,pady=10,sticky='w')
    
    dob_date_entry=DateEntry(detail_frame,width=18,font=('times new roman',12),state='readonly',date_pattern='dd/mm/yyyy')
    dob_date_entry.grid(row=1,column=3)
    
    contact_label=Label(detail_frame,text='Contact',font=('times new roman',12),bg='white')
    contact_label.grid(row=1,column=4,padx=20,pady=10,sticky='w')
    
    contact_entry=Entry(detail_frame,font=('times new roman',12),bg='lightyellow')
    contact_entry.grid(row=1,column=5,padx=20,pady=10)

    Employment_label=Label(detail_frame,text='Employment Type',font=('times new roman',12),bg='white')
    Employment_label.grid(row=2,column=0,padx=20,pady=10,sticky='w')
    
    Employment_combobox=ttk.Combobox(detail_frame,values=('Full Time','Part Time','Casual','Contract','Intern'),font=('times new roman',12),width=18,state='readonly')
    Employment_combobox.set('Types')
    Employment_combobox.grid(row=2,column=1)
    
    
    Education_label=Label(detail_frame,text='Education',font=('times new roman',12),bg='white')
    Education_label.grid(row=2,column=2,padx=20,pady=10,sticky='w')
    
    Education_combobox=ttk.Combobox(detail_frame,values=('BTech','MCA','Degree','MBA','MCOM','MSC','Diploma'),font=('times new roman',12),width=18,state='readonly')
    Education_combobox.set('Select')
    Education_combobox.grid(row=2,column=3)
    
    Work_label=Label(detail_frame,text='Work Shift',font=('times new roman',12),bg='white')
    Work_label.grid(row=2,column=4,padx=20,pady=10,sticky='w')
    
    Work_combobox=ttk.Combobox(detail_frame,values=('Morning','Evening','Afternoon','Night'),font=('times new roman',12),width=18,state='readonly')
    Work_combobox.set('Select')
    Work_combobox.grid(row=2,column=5)
    
    address_label=Label(detail_frame,text='Address',font=('times new roman',12),bg='white')
    address_label.grid(row=3,column=0,padx=20,pady=10,sticky='w')
    address_text=Text(detail_frame,width=20,height=3,font=('times new roman',12),bg='lightyellow')
    address_text.grid(row=3,column=1,rowspan=2)
    
    doj_label=Label(detail_frame,text='Date of Joining',font=('times new roman',12),bg='white')
    doj_label.grid(row=3,column=2,padx=20,pady=10,sticky='w')
    
    doj_date_entry=DateEntry(detail_frame,width=18,font=('times new roman',12),state='readonly',date_pattern='dd/mm/yyyy')
    doj_date_entry.grid(row=3,column=3)
    
    User_label=Label(detail_frame,text='User Type',font=('times new roman',12),bg='white')
    User_label.grid(row=4,column=2,padx=20,pady=10,sticky='w')
    
    User_combobox=ttk.Combobox(detail_frame,values=('Admin','Employee'),font=('times new roman',12),width=18,state='readonly')
    User_combobox.set('Select User Type')
    User_combobox.grid(row=4,column=3)
    
    
    salary_label=Label(detail_frame,text='Salary',font=('times new roman',12),bg='white')
    salary_label.grid(row=3,column=4,padx=20,pady=10,sticky='w')
    
    salary_entry=Entry(detail_frame,font=('times new roman',12),bg='lightyellow')
    salary_entry.grid(row=3,column=5,padx=20,pady=10)   
    
    password_label=Label(detail_frame,text='Password',font=('times new roman',12),bg='white')
    password_label.grid(row=4,column=4,padx=20,pady=10,sticky='w')
    
    password_entry=Entry(detail_frame,font=('times new roman',12),bg='lightyellow')
    password_entry.grid(row=4,column=5,padx=20,pady=10)
    
    button_frame = Frame(employee_frame,bg='white')
    button_frame.place(x=200,y=520)
    
    add_button = Button(button_frame,text='Add',font=('times new roman',12),width=10,cursor='hand2',fg='white',
                        bg='#0f4d7d',command=lambda:add_employee(empid_entry.get(),name_entry.get(),email_entry.get(),gender_combobox.get(),
                                                          dob_date_entry.get(),contact_entry.get(),Employment_combobox.get(),
                                                          Education_combobox.get(),Work_combobox.get(),address_text.get(1.0,END),
                                                          doj_date_entry.get(),salary_entry.get(),User_combobox.get(),password_entry.get()))
    add_button.grid(row=0,column=0,padx=20)
    
    update_button = Button(button_frame,text='Update',font=('times new roman',12),width=10,cursor='hand2',fg='white',
                        bg='#0f4d7d',command=lambda:update_employee(empid_entry.get(),name_entry.get(),email_entry.get(),gender_combobox.get(),
                                                          dob_date_entry.get(),contact_entry.get(),Employment_combobox.get(),
                                                          Education_combobox.get(),Work_combobox.get(),address_text.get(1.0,END),
                                                          doj_date_entry.get(),salary_entry.get(),User_combobox.get(),password_entry.get()))
    update_button.grid(row=0,column=1,padx=20)
    
    
    delete_button = Button(button_frame,text='Delete',font=('times new roman',12),width=10,cursor='hand2',fg='white',
                        bg='#0f4d7d',command=lambda:delete_employee(empid_entry.get()))
    delete_button.grid(row=0,column=2,padx=20)
    
    clear_button = Button(
    button_frame,
    text='Clear',
    font=('times new roman', 12),
    width=10,
    cursor='hand2',
    fg='white',
    bg='#0f4d7d',
    command=lambda: clear_fields(
        empid_entry,
        name_entry,
        email_entry,
        gender_combobox,
        dob_date_entry,
        contact_entry,
        Employment_combobox,
        Education_combobox,
        Work_combobox,
        address_text,
        doj_date_entry,
        salary_entry,
        User_combobox,
        password_entry,    
))

    clear_button.grid(row=0,column=3,padx=20)
    
    employee_treeview.bind(
    '<ButtonRelease-1>',
    lambda event: select_data(
        event,
        empid_entry,
        name_entry,
        email_entry,
        gender_combobox,      
        dob_date_entry,       
        contact_entry,
        Employment_combobox,
        Education_combobox,
        Work_combobox,
        address_text,
        doj_date_entry,
        salary_entry,
        User_combobox,
        password_entry
    )
)
    create_database_table() 
    return employee_frame
    
    
    
    
    
    
    
    
    