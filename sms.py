from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
import matplotlib.pyplot as plt
import socket
import requests
from sqlite3 import *
import bs4
import lxml
import winsound

# Add button
def f1():
	root.withdraw()
	add_st.deiconify()


#view button
def f2():
	view_stData.delete(1.0, END)
	root.withdraw()
	view_st.deiconify()
	con = None
	try:
		con = connect("stu_test.db")
		cursor = con.cursor()
		sql = "select * from student"
		cursor.execute(sql)
		data = cursor.fetchall()
		info = ""
		for d in data:
			info = info + "rno: " + str(d[0]) +" name: "+str(d[1]) +" marks:"+ str(d[2]) +"\n"
		view_stData.insert(INSERT, info)
	except Exception as e:
		print("Issue: ",e)
	finally:
		if con is not None:
			con.close()

#back from add
def f3():
	add_st.withdraw()
	root.deiconify()

#back from view
def f4():
	view_st.withdraw()
	root.deiconify()

#update button
def f5():
	root.withdraw()
	updt_st.deiconify()

#back from update
def f6():
	updt_st.withdraw()
	root.deiconify()
#delete button
def f7():
	root.withdraw()
	del_st.deiconify()
#back from delete
def f8():
	del_st.withdraw()
	root.deiconify()
#charts
def f9():
	con = None
	student, marks = [], []
	try:
		con = connect("stu_test.db")
		cursor = con.cursor()
		sql = "SELECT * FROM  student ORDER BY marks LIMIT 5"
		data = cursor.execute(sql)
		for d in data:
			student.append(d[1])
			marks.append(int(d[2]))
		
		plt.bar(student, marks)
		plt.ylabel('Marks')
		plt.title("Batch Information")
		#plt.grid()
		plt.show()
	except Exception as e:
		showerror("Issue", e)
	finally:
		if con is not None:
			con.close()
	
# add-insert
def f10():
	con = None
	try:
		con = connect("stu_test.db")
		cursor = con.cursor()
		rno = rnoEnter.get()
		#messagebox.showerro("error","invalid Roll no")
		marks = marksEnter.get()
		name = nameEnter.get()
		'''sql = "insert into student values ('%d','%s','%d')"
		args=(rno,name,marks)
		cursor.execute(sql % args)
		con.commit()
		msg=str(cursor.rowcount)+" records inserted "
		showinfo("Results ",msg)
		rnoEnter.delete(0,END)
		nameEnter.delete(0,END)
		marksEnter.delete(0,END)
		rnoEnter.focus()'''
		if str(rno).isdigit():
			if name.isalpha() and len(name)>=2 and name!="":
				if str(marks).isdigit() and (int(marks)>0 and int(marks)<=100) and marks!="":
					rno=int(rno)
					marks=int(marks)
					sql="insert into student values ('%d','%s','%d')"
					args=(rno,name,marks)
					cursor.execute(sql % args)
					con.commit()
					winsound.PlaySound('positive.wav', winsound.SND_ALIAS| winsound.SND_ASYNC)
					msg=str(cursor.rowcount)+" records inserted "
					showinfo("Results ",msg)
					rnoEnter.delete(0,END)
					nameEnter.delete(0,END)
					marksEnter.delete(0,END)
					rnoEnter.focus()
				else:
					msg=str(marks)+" invalid marks"
					winsound.PlaySound('negative.wav', winsound.SND_ALIAS| winsound.SND_ASYNC)
					showerror("Error",msg)
					marksEnter.delete(0,END)
					marksEnter.focus()
			else:
				msg=name+" Invalid Name "
				winsound.PlaySound('negative.wav', winsound.SND_ALIAS| winsound.SND_ASYNC)
				showerror("Error",msg)
				nameEnter.delete(0,END)
				nameEnter.focus()

		else:
			msg=str(rno)+" should be integer"
			winsound.PlaySound('negative.wav', winsound.SND_ALIAS| winsound.SND_ASYNC)
			showerror("Error",msg)
			rnoEnter.delete(0,END)
			rnoEnter.focus()
	except Exception as e:
		winsound.PlaySound('tryAgain.wav', winsound.SND_ALIAS| winsound.SND_ASYNC)
		showerror("wrong query ","Roll number already exists")
		con.rollback()
		rnoEnter.delete(0,END)
		nameEnter.delete(0,END)
		marksEnter.delete(0,END)
		rnoEnter.focus()
	finally:
		
		if con is not None:
			con.close()
# Update
def f11():
	con = None
	
	try:
		con = connect("stu_test.db")
		cursor = con.cursor()
		rno = urnoEnter.get()
		name = unameEnter.get()
		marks = umarksEnter.get()
		if str(rno).isdigit() and rno!="":
			if str(name).isalpha() and len(name)>=2 and name!="":
				if str(marks).isdigit() and (int(marks)>0 and int(marks)<=100) and marks!="":
					rno=int(rno)
					marks=int(marks)
					sql="update student set name='%s',marks='%d' where rno='%d'"
					args=(name,marks,rno)
					cursor.execute(sql % args)
					con.commit()
					if cursor.rowcount>0:
						msg=str(cursor.rowcount)+" rows updated"
						showinfo("Results",msg)
						urnoEnter.delete(0,END)
						unameEnter.delete(0,END)
						umarksEnter.delete(0,END)
						urnoEnter.focus()
					else:
						winsound.PlaySound('tryAgain.wav', winsound.SND_ALIAS| winsound.SND_ASYNC)
						showwarning("Alert","Record does not Exist")
						urnoEnter.delete(0,END)
						unameEnter.delete(0,END)
						umarksEnter.delete(0,END)
						urnoEnter.focus()
				else:
					winsound.PlaySound('negative.wav', winsound.SND_ALIAS| winsound.SND_ASYNC)
					showerror("Error","Invalid marks")
					urnoEnter.delete(0,END)
					urnoEnter.focus()
			else:
				winsound.PlaySound('negative.wav', winsound.SND_ALIAS| winsound.SND_ASYNC)
				showerror("Error","Invalid name")
				unameEnter.delete(0,END)
				unameEnter.focus()
		else:
			winsound.PlaySound('negative.wav', winsound.SND_ALIAS| winsound.SND_ASYNC)
			showerror("Error","Invalid rollno")
			urnoEnter.delete(0,END)
			urnoEnter.focus()
	except Exception as e:
		showerror("query error ",e)
		con.rollback()				
	finally:
		if con is not None:
			con.close()
# delete
def f12():
	con = None
	try:
		con = connect("stu_test.db")
		cursor = con.cursor()
		rno=drnoEnter.get()
		if str(rno).isdigit() and rno!="":
			rno=int(rno)
			sql="delete from student where rno='%d'"
			args=(rno)
			cursor.execute(sql % args)
			if cursor.rowcount>0:
				msg=str(cursor.rowcount)+" rows deleted"
				winsound.PlaySound('positive.wav', winsound.SND_ALIAS| winsound.SND_ASYNC)
				showinfo("Results",msg)
				con.commit()
				drnoEnter.delete(0,END)
				drnoEnter.focus()
			else:
				winsound.PlaySound('tryAgain.wav', winsound.SND_ALIAS| winsound.SND_ASYNC)
				showwarning("Alert","Record does not exist")
				drnoEnter.delete(0,END)
				drnoEnter.focus()
		else:
			winsound.PlaySound('negative.wav', winsound.SND_ALIAS| winsound.SND_ASYNC)
			showerror("Error","Invalid rollno")
			drnoEnter.delete(0,END)
			drnoEnter.focus()
	
	except Exception as e:
		con.rollback()
		showerror("Issue", e)
	finally:
		if con is not None:
			con.close()
		drnoEnter.delete(0, END)


		

#msg filter
def alter(msg):
	if msg.find(',') != -1 or msg.find(';') != -1:
		motd = msg.replace(',' , '\n')
		motd = msg.replace(';' , '\n')
	else:
		motd, i, j = '', 0, 0
		mesappend = ''
		val = msg.rfind('-')
		partone = msg[0:val]
		parttwo = msg[val:]
		for k in partone:
			if k == ' ' and j % 6 == 0:
				mesappend = mesappend + k + '\n'
				j += 1
			elif k == ' ':
				mesappend = mesappend + k
				j += 1
			else:
				mesappend = mesappend + k
		motd = mesappend + '\n' +parttwo
	return motd

#Location-Temperature quote

info, qotd = '',''
try:
	socket.create_connection(("www.google.com", 80))
	res = requests.get("https://ipinfo.io")
	data = res.json()
	city_name = data['city']
	a1 = "https://api.openweathermap.org/data/2.5/weather?units=metric"
	a2 = "&q=" + city_name
	a3 = "&appid=c6e315d09197cec231495138183954bd"
	res = requests.get(a1 + a2 + a3)
	data = res.json()
	temp = data['main']['temp']
	info = "Location: " + str(city_name) + "\tTemperature: " + str(temp)
	res = requests.get("https://www.brainyquote.com/quote_of_the_day")
	soup = bs4.BeautifulSoup(res.text,'lxml')
	data = soup.find("img", {"class":"p-qotd"})
	msg = data['alt']
	msg = alter(msg)
	qotd = "QOTD: " + str(msg)
except Exception as e:
	showerror("Connection issue", e)
	print(e)

# SMS

root = Tk()
root.title("S.M.S")
root.geometry("500x575+400+25")
root.configure(background="PaleGreen1")

btnAdd = Button(root, text="Add",font=("Arial",18,"bold"),width=10, command = f1)
btnView = Button(root, text="View",font=("Arial",18,"bold"),width=10, command = f2)
btnUpdate = Button(root,text = "Update",font=("Arial",18,"bold"),width=10, command = f5)
btnDelete= Button(root, text="Delete",font=("Arial",18,"bold"),width=10, command = f7)
btnCharts = Button(root, text="Charts",font=("Arial",18,"bold"),width=10, command = f9)
lbInfo = Label(root, text = info ,font = ("Arial",18,"bold"), borderwidth = 1, bg = "PaleGreen1", relief = "solid")
lbQotd = Label(root, text = qotd ,font = ("Arial",18,"bold"),borderwidth = 1, bg="PaleGreen1", relief="solid")

btnAdd.pack(pady = 10)
btnView.pack(pady = 10)
btnUpdate.pack(pady = 10)
btnDelete.pack(pady = 10)
btnCharts.pack(pady = 10)
lbInfo.pack(pady = 10)
lbQotd.pack(pady = 10)

# add student  toplevel helps in creating a new window

add_st = Toplevel(root)
add_st.title("Add St.")
add_st.geometry("500x500+400+100")
add_st.configure(background = "LightBlue1")
add_st.withdraw()

lblrno = Label(add_st, text = "enter rno:", font = ("Arial",18,"bold"), bg="LightBlue1")
rnoEnter = Entry(add_st, bd = 5,font = ("Arial",18,"bold"))
lb1name = Label(add_st, text = "enter name:", font = ("Arial",18,"bold"), bg="LightBlue1")
nameEnter = Entry(add_st, bd = 5,font = ("Arial",18,"bold"))
lblmarks = Label(add_st, text = "enter marks:", font = ("Arial",18,"bold"), bg="LightBlue1")
marksEnter = Entry(add_st, bd = 5,font = ("Arial",18,"bold"))
add_stSave = Button(add_st, text = "Save", font =  ("Arial",18,"bold"), command = f10)
add_stBack = Button(add_st, text = "Back", font = ("Arial", 18, "bold"), command = f3)
lblrno.pack(pady = 10)
rnoEnter.pack(pady = 10)
lb1name.pack(pady = 10)
nameEnter.pack(pady = 10)
lblmarks.pack(pady = 10)
marksEnter.pack(pady = 10)
add_stSave.pack(pady = 10)
add_stBack.pack(pady = 10)
rnoEnter.focus()

# view st.

view_st = Toplevel(root)
view_st.title("View St.")
view_st.geometry("650x500+400+100")
view_st.configure(background = "pink1")
view_st.withdraw()
view_stData = ScrolledText(view_st, width = 40, height = 20)
view_stBack = Button(view_st, text = "Back", font = ("Arial", 18, "bold"), command = f4)

view_stData.pack(pady = 10)
view_stBack.pack(pady = 10)

# update st.

updt_st = Toplevel(root)
updt_st.title("Update St.")
updt_st.geometry("500x500+400+100")
updt_st.configure(background = "bisque")
updt_st.withdraw()

ulblrno = Label(updt_st, text = "enter rno:", font = ("Arial",18,"bold"), bg="bisque")
urnoEnter = Entry(updt_st, bd = 5,font = ("Arial",18,"bold"))
ulb1name = Label(updt_st, text = "enter name:", font = ("Arial",18,"bold"), bg="bisque")
unameEnter = Entry(updt_st, bd = 5,font = ("Arial",18,"bold"))
ulblmarks = Label(updt_st, text = "enter marks:", font = ("Arial",18,"bold"), bg="bisque")
umarksEnter = Entry(updt_st, bd = 5,font = ("Arial",18,"bold"))
uadd_stSave = Button(updt_st, text = "Update", font =  ("Arial",18,"bold"), command = f11)
uadd_stBack = Button(updt_st, text = "Back", font = ("Arial", 18, "bold"), command = f6)


ulblrno.pack(pady = 10)
urnoEnter.pack(pady = 10)
ulb1name.pack(pady = 10)
unameEnter.pack(pady = 10)
ulblmarks.pack(pady = 10)
umarksEnter.pack(pady = 10)
uadd_stSave.pack(pady = 10)
uadd_stBack.pack(pady = 10)
urnoEnter.focus()

# delete student

del_st = Toplevel(root)
del_st.title("Delete St.")
del_st.geometry("500x500+400+100")
del_st.configure(background = "salmon1")
del_st.withdraw()

dlblrno = Label(del_st, text = "enter rno:", font = ("Arial", 18, "bold"), bg = "salmon1")
drnoEnter = Entry(del_st, font = ("Arial", 18, "bold"), bd = 5)
del_stSave = Button(del_st, text = "Delete", font = ("Arial", 18, "bold"), command = f12)
del_stBack = Button(del_st, text = "Back", font = ("Arial", 18, "bold"), command = f8)
dlblrno.pack(pady = 10)
drnoEnter.pack(pady = 10)
del_stSave.pack(pady = 10)
del_stBack.pack(pady = 10)
drnoEnter.focus()

root.mainloop()






