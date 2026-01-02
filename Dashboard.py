from tkinter import *
from tkinter import  ttk
from tkcalendar import DateEntry
from tkinter import messagebox

import pymysql
from employee import employee_form
from supplier import supplier_form
from category import category_form
from product import product_form
from employee import connect_database
import time


def update():
    connection, cursor = connect_database()   # connection first, cursor second
    if not cursor or not connection:
        return

    cursor.execute("USE inventorysystem")
    cursor.execute("SELECT * FROM employees_data")
    emp_records = cursor.fetchall()
    emp_count_label.config(text=len(emp_records))
    
    cursor.execute("SELECT * from supplier_data")
    sup_records= cursor.fetchall()
    sup_count_label.config(text=len(sup_records))
    
    cursor.execute("SELECT * from  category_data")
    cat_records= cursor.fetchall()
    cat_count_label.config(text=len(cat_records))
    
    cursor.execute("SELECT * from  product_data")
    prod_records= cursor.fetchall()
    prod_count_label.config(text=len(prod_records)) 
    date_time = time.strftime('%I:%M:%S %p on %A, %B %d, %Y')
    subtitleLabel.config(text=f'Welcome Admin\t\t\t\t\t\t\t{date_time}')
    subtitleLabel.after(1000,update)


def tax_window():
    def save_tax():
        value = tax_count.get()

        connection, cursor = connect_database() 
        if not cursor or not connection:
            return       
        cursor.execute('use inventorysystem')
        cursor.execute('CREATE TABLE IF NOT EXISTS tax_table (id INT PRIMARY KEY, tax DECIMAL(5,2))')
        cursor.execute('SELECT id from tax_table WHERE id =1')
        if cursor.fetchone():
            cursor.execute('UPDATE tax_table SET tax=%s WHERE id= 1',value)
        else:
            cursor.execute('INSERT INTO tax_table(id,tax) Values(1, %s)',value)        
        connection.commit()
        messagebox.showinfo('Success',f'Tax is set to {value}% and saved successfully', parent=tax_root)
        
    tax_root = Toplevel()
    tax_root.title('Tax Window')
    tax_root.geometry('300x200')
    tax_root.grab_set()
    tax_percentage=Label(tax_root,text='Enter Tax Percentage(%)',font=('arial',12))
    tax_percentage.pack(pady=10)
    tax_count=Spinbox(tax_root, from_=0, to=100,font=('arial',12))
    tax_count.pack(pady=10)
    save_button=Button(tax_root, text='Save',font=('arial',12,'bold'),bg='#4d636d',fg='white',width=10,command=save_tax)
    save_button.pack(pady=20)


current_frame=None
def show_form(form_function):
    global current_frame
    if current_frame :
        current_frame.place_forget()
    current_frame=form_function(window)
    
    
    
window = Tk()

window.title('Dashboard')
window.geometry('1270x675+0+0')
window.resizable(0, 0)
window.config(bg='White')

bg_image = PhotoImage(file=r"C:\Users\ADMIN\Desktop\Inventory Management System\inventory.png")

titleLabel = Label(window, image=bg_image, compound=LEFT,text='  Inventory Management System',font=('times new roman', 40, 'bold'),bg='#010c48', fg='white', anchor='w', padx=20)
titleLabel.place(x=0, y=0, relwidth=1)

# Logout Button
LogoutButton = Button(window, text='Logout', font=('times new roman', 20, 'bold'), fg='#010c48')
LogoutButton.place(x=1100, y=10)


subtitleLabel = Label(window, text='Welcome Admin\t\t Date:08-12-2025\t\t Time:11:20:30 am',font=('times new roman', 15), bg='#4d636d', fg='white')
subtitleLabel.place(x=0, y=70, relwidth=1)

leftFrame = Frame(window)
leftFrame.place(x=0, y=102, width=200, height=570)

logoImage = PhotoImage(file='inventory-log.png')
imageLabel = Label(leftFrame, image=logoImage)
imageLabel.pack()

# Buttons with Icons
employee_icon = PhotoImage(file='employee.png')
employee_button = Button(leftFrame, image=employee_icon, compound=LEFT,text='Employees', font=('times new roman', 20, 'bold'),anchor='w', command=lambda:show_form(employee_form))
employee_button.pack(fill=X)

supplier_icon = PhotoImage(file='supplier.png')
supplier_button = Button(leftFrame, image=supplier_icon, compound=LEFT,text=' Supplier', font=('times new roman',
                                                            20, 'bold'), anchor='w',padx=10,command=lambda:show_form(supplier_form))
supplier_button.pack(fill=X)

category_icon = PhotoImage(file='categorization.png')
category_button = Button(leftFrame, image=category_icon, compound=LEFT,text=' Category', font=('times new roman', 20, 'bold'), anchor='w',
                         padx=10,command=lambda:show_form(category_form))
category_button.pack(fill=X)

Product_icon = PhotoImage(file='Product.png')
Product_button = Button(leftFrame, image=Product_icon, compound=LEFT,text=' Product', font=('times new roman', 20, 'bold'), anchor='w',
                        padx=10,command=lambda:show_form(product_form))
Product_button.pack(fill=X)

Sales_icon = PhotoImage(file='sales.png')
Sales_button = Button(leftFrame, image=Sales_icon, compound=LEFT,text=' Sales', font=('times new roman', 20, 'bold'), anchor='w')
Sales_button.pack(fill=X)


Tax_icon = PhotoImage(file='tax.png')
Tax_button = Button(leftFrame, image=Tax_icon, compound=LEFT,text=' Tax', font=('times new roman', 20, 'bold'), anchor='w',command=tax_window)
Tax_button.pack(fill=X)


exit_icon = PhotoImage(file='Exit.png')
exit_button = Button(leftFrame, image=exit_icon, compound=LEFT,text=' Exit', font=('times new roman', 20, 'bold'), anchor='w')
exit_button.pack(fill=X)


emp_frame = Frame(window, bg='#2c3e50', bd=3, relief=RIDGE)
emp_frame.place(x=400, y=125, height=170, width=280)
total_emp_icon = PhotoImage(file='emp.png')
Label(emp_frame, image=total_emp_icon).pack(pady=10)
Label(emp_frame, text='Total Employees', bg='#2c3e50', fg='white',
      font=('times new roman', 15, 'bold')).pack()
emp_count_label = Label(emp_frame, text=0, bg='#2c3e50', fg='white',
                        font=('times new roman', 30, 'bold'))
emp_count_label.pack()

sup_frame = Frame(window, bg='#8e44ad', bd=3, relief=RIDGE)
sup_frame.place(x=800, y=125, height=170, width=280)
total_sup_icon = PhotoImage(file='sup.png')
Label(sup_frame, image=total_sup_icon).pack(pady=10)
Label(sup_frame, text='Total Suppliers', bg='#8e44ad', fg='white',
      font=('times new roman', 15, 'bold')).pack()
sup_count_label = Label(sup_frame, text=0, bg='#8e44ad', fg='white',
                        font=('times new roman', 30, 'bold'))
sup_count_label.pack()

cat_frame = Frame(window, bg='#27ae60', bd=3, relief=RIDGE)
cat_frame.place(x=400, y=310, height=170, width=280)

total_cat_icon = PhotoImage(file='category.png')
Label(cat_frame, image=total_cat_icon).pack(pady=10)
Label(cat_frame, text='Total Categories', bg='#27ae60', fg='white',
      font=('times new roman', 15, 'bold')).pack()
cat_count_label = Label(cat_frame, text=0, bg='#27ae60', fg='white',
                        font=('times new roman', 30, 'bold'))
cat_count_label.pack()

prod_frame = Frame(window, bg='#2c3e50', bd=3, relief=RIDGE)
prod_frame.place(x=800, y=310, height=170, width=280)
total_prod_icon = PhotoImage(file='products.png')
Label(prod_frame, image=total_prod_icon).pack(pady=10)
Label(prod_frame, text='Total Products', bg='#2c3e50', fg='white',
      font=('times new roman', 15, 'bold')).pack()
prod_count_label = Label(prod_frame, text=0, bg='#2c3e50', fg='white',
                         font=('times new roman', 30, 'bold'))
prod_count_label.pack()


sal_frame = Frame(window, bg='#e74c3c', bd=3, relief=RIDGE)
sal_frame.place(x=600, y=490, height=150, width=280)
total_sal_icon = PhotoImage(file='sal.png')
Label(sal_frame, image=total_sal_icon).pack(pady=10)
Label(sal_frame, text='Total Sales', bg='#e74c3c', fg='white',font=('times new roman', 15, 'bold')).pack()
Label(sal_frame, text=112, bg='#e74c3c', fg='white',font=('times new roman', 30, 'bold')).pack()

update()

window.mainloop()
