import pandas as pd
import os
import tkinter as tk
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def read_data():
    if not os.path.exists('./transaction.csv'):
        #create the empty csv file if it doesnt exist
        with open("transaction.csv", "w") as infile:
            #write headers
            infile.write('ID,Date,Description,Withdrawal,Deposit,Balance\n')
            infile.write('-,-,-,-,-,0.0')
            
    df = pd.read_csv('transaction.csv')
    return df

def get_current_balance(df) :
    last_balance = df.iloc[-1].Balance
    return last_balance
 
#main GUI part 
class App(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.df = read_data() # panda dataframe 
        
        self.parent_title = parent.title("Transaction Recorder/Generator")
        #for error after submission 
        self.lbl_error = tk.Label(self.parent, text = '', font = ('Helvetica', 12, 'italic'), fg = 'red', relief = 'solid')
        self.lbl_error['borderwidth'] = 0
        self.lbl_error.grid(row = 0, columnspan = 7, padx = 10,pady = 10, sticky = "nsew")

        #transaction date 
        self.lbl_date =  tk.Label(self.parent, text = 'Date : ', font = ('Helvetica', 12, 'bold')).grid(row = 1, column = 0, padx = 10, sticky ='w')
        self.day_label = tk.Label(self.parent, text = 'day', font = ('Helvetica', 12)).grid(row = 1, column = 1, ipadx = 5)
        self.daylist = [i for i in range(1,32)]
        self.day_variable = tk.IntVar(self.parent)
        self.day_variable.set(self.daylist[0])
        self.day_opt = tk.OptionMenu(self.parent, self.day_variable, *self.daylist)
        self.day_opt.config(width = 1, font = ('Helvetica', 12))
        self.day_opt.grid(row = 1, column = 2, sticky = "ew" )
        
        self.month_label = tk.Label(self.parent, text = 'month', font = ('Helvetica', 12)).grid(row = 1, column = 3, ipadx = 5)
        self.monthlist = [i for i in range(1,13)]
        self.month_variable = tk.IntVar(self.parent)
        self.month_variable.set(self.monthlist[0])
        self.month_opt = tk.OptionMenu(self.parent, self.month_variable, *self.monthlist)
        self.month_opt.config(width =1, font = ('Helvetica', 12))
        self.month_opt.grid(row = 1, column = 4, sticky = "ew")

        self.year_label = tk.Label(self.parent, text = 'year', font = ('Helvetica', 12)).grid(row = 1,column = 5, ipadx = 5)
        self.yearlist = [i for i in range(2020,2030)]
        self.year_variable = tk.IntVar(self.parent)
        self.year_variable.set(self.yearlist[0])
        self.year_opt = tk.OptionMenu(self.parent, self.year_variable, *self.yearlist)
        self.year_opt.config(width = 4, font = ('Helvetica',12))
        self.year_opt.grid(row = 1, column = 6, sticky ="ew")

        #Description
        self.lbl_date =  tk.Label(self.parent, text = 'Description : ', font = ('Helvetica', 12, 'bold')).grid(row = 2, column = 0, padx = 10, pady = 10,sticky = 'w')
        self.txt_description = tk.Text(height = 2,width = 48,master = self.parent)
        self.txt_description.grid(row = 2, column = 1, columnspan = 6)

        #Type of Transaction
        self.transaction_label = tk.Label(self.parent, text = 'Type : ', font = ('Helvetica',12,'bold')).grid(row = 3, column = 0, padx = 10, pady = 10, sticky = 'w')
        self.translist = ['Deposit','Withdrawal']
        self.trans_variable = tk.StringVar(self.parent)
        self.trans_variable.set(self.translist[0])
        self.trans_opt = tk.OptionMenu(self.parent, self.trans_variable, *self.translist)
        self.trans_opt.config(width = 10, font = ('Helvetica',12))
        self.trans_opt.grid(row = 3, column = 1, columnspan =4, sticky ='w')

        #amount
        self.lbl_amount =  tk.Label(self.parent, text = 'Amount: ', font = ('Helvetica', 12, 'bold')).grid(row = 4, column = 0, padx = 10, pady = 10,sticky = 'w')
        self.ety_amount = tk.Entry(self.parent, width = 16)
        self.ety_amount.grid(row = 4, column =1 ,columnspan = 3, sticky = 'w')
        self.lbl_info =  tk.Label(self.parent, text = 'eg. 10,000.50 \N{RIGHTWARDS BLACK ARROW} 10000.50', font = ('Helvetica', 12, 'italic')).grid(row = 4, column = 4, columnspan = 4, padx = 10, pady = 10,sticky = 'ew')

        #commit & clear
        self.clear_button = tk.Button(self.parent, text = 'Clear', font = ('Helvetica', 12, 'bold'), command = self.clear, relief = tk.RAISED)
        self.clear_button.grid(row = 5, column = 4,columnspan =2, sticky = 'e', ipadx = 0, ipady = 5)

        self.commit_button = tk.Button(self.parent, text = 'Commit', font = ('Helvetica', 12, 'bold'), command = self.commit_transaction, relief = tk.RAISED)
        self.commit_button.grid(row = 5, column = 6, sticky = 'e', ipadx = 5, ipady = 5)

        #delete transaction
        self.lbl_delete = tk.Label(self.parent, text = 'Delete Transaction' , font = ('Helvetica' , 12, 'bold italic'))
        self.lbl_delete.grid(row = 6 ,column = 0, columnspan = 5, padx = 10,pady = 10, sticky ='w')
        self.lbl_refid =  tk.Label(self.parent, text = 'Ref ID: ', font = ('Helvetica', 12, 'bold')).grid(row = 7, column = 0, padx = 10, pady = 10,sticky = 'w')
        self.ety_refid = tk.Entry(self.parent, width = 10)
        self.ety_refid.grid(row = 7, column =1 , columnspan = 2,  sticky = 'w')

        self.delete_button = tk.Button(self.parent, text = 'Delete', font = ('Helvetica', 12, 'bold'), command = self.delete_id, relief = tk.RAISED)
        self.delete_button.grid(row = 8, column = 6, sticky = 'e', ipadx = 5, ipady = 5)

        #last 5 transactions
        self.display_last_five()

        #Generate Partial Report
        self.lbl_delete = tk.Label(self.parent, text = 'Generate Report' , font = ('Helvetica' , 12, 'bold italic'))
        self.lbl_delete.grid(row = 11 ,column = 0, columnspan = 5, padx = 10,pady = 10, sticky ='w')
        
        self.lbl_date_from =  tk.Label(self.parent, text = 'From : ', font = ('Helvetica', 12, 'bold')).grid(row = 12, column = 0, padx = 10, sticky ='w')
        self.day_label_from = tk.Label(self.parent, text = 'day', font = ('Helvetica', 12)).grid(row = 12, column = 1, ipadx = 5)
        self.daylist_from = [i for i in range(1,32)]
        self.day_variable_from = tk.IntVar(self.parent)
        self.day_variable_from.set(self.daylist_from[0])
        self.day_opt_from = tk.OptionMenu(self.parent, self.day_variable_from, *self.daylist_from)
        self.day_opt_from.config(width = 1, font = ('Helvetica', 12))
        self.day_opt_from.grid(row = 12, column = 2, sticky = "ew" )
        
        self.month_label_from = tk.Label(self.parent, text = 'month', font = ('Helvetica', 12)).grid(row = 12, column = 3, ipadx = 5)
        self.monthlist_from = [i for i in range(1,13)]
        self.month_variable_from = tk.IntVar(self.parent)
        self.month_variable_from.set(self.monthlist_from[0])
        self.month_opt_from = tk.OptionMenu(self.parent, self.month_variable_from, *self.monthlist_from)
        self.month_opt_from.config(width =1, font = ('Helvetica', 12))
        self.month_opt_from.grid(row = 12, column = 4, sticky = "ew")

        self.year_label_from = tk.Label(self.parent, text = 'year', font = ('Helvetica', 12)).grid(row = 12,column = 5, ipadx = 5)
        self.yearlist_from = [i for i in range(2020,2030)]
        self.year_variable_from = tk.IntVar(self.parent)
        self.year_variable_from.set(self.yearlist_from[0])
        self.year_opt_from = tk.OptionMenu(self.parent, self.year_variable_from, *self.yearlist_from)
        self.year_opt_from.config(width = 4, font = ('Helvetica',12))
        self.year_opt_from.grid(row = 12, column = 6, sticky ="ew")
        
        self.lbl_date_to =  tk.Label(self.parent, text = 'To : ', font = ('Helvetica', 12, 'bold')).grid(row = 13, column = 0, padx = 10, sticky ='w')
        self.day_label_to = tk.Label(self.parent, text = 'day', font = ('Helvetica', 12)).grid(row = 13, column = 1, ipadx = 5)
        self.daylist_to = [i for i in range(1,32)]
        self.day_variable_to = tk.IntVar(self.parent)
        self.day_variable_to.set(self.daylist_to[0])
        self.day_opt_to = tk.OptionMenu(self.parent, self.day_variable_to, *self.daylist_to)
        self.day_opt_to.config(width = 1, font = ('Helvetica', 12))
        self.day_opt_to.grid(row = 13, column = 2, sticky = "ew" )
        
        self.month_label_to = tk.Label(self.parent, text = 'month', font = ('Helvetica', 12)).grid(row = 13, column = 3, ipadx = 5)
        self.monthlist_to = [i for i in range(1,13)]
        self.month_variable_to = tk.IntVar(self.parent)
        self.month_variable_to.set(self.monthlist_to[0])
        self.month_opt_to = tk.OptionMenu(self.parent, self.month_variable_to, *self.monthlist_to)
        self.month_opt_to.config(width =1, font = ('Helvetica', 12))
        self.month_opt_to.grid(row = 13, column = 4, sticky = "ew")

        self.year_label_to = tk.Label(self.parent, text = 'year', font = ('Helvetica', 12)).grid(row = 13,column = 5, ipadx = 5)
        self.yearlist_to = [i for i in range(2020,2030)]
        self.year_variable_to = tk.IntVar(self.parent)
        self.year_variable_to.set(self.yearlist_to[0])
        self.year_opt_to = tk.OptionMenu(self.parent, self.year_variable_to, *self.yearlist_to)
        self.year_opt_to.config(width = 4, font = ('Helvetica',12))
        self.year_opt_to.grid(row = 13, column = 6, sticky ="ew")

        #Generate partial report button
        self.generate_button = tk.Button(self.parent, text = 'Generate Report From/To', font = ('Helvetica', 12, 'bold'), command = self.partial_summary, relief = tk.RAISED)
        self.generate_button.grid(row = 14, column = 0, columnspan = 3, sticky = 'e', ipadx = 5, ipady = 5, pady = 20)
        
        #Generate Full Report
        self.generate_button = tk.Button(self.parent, text = 'Generate Full Reports', font = ('Helvetica', 12, 'bold'), command = self.summary, relief = tk.RAISED)
        self.generate_button.grid(row = 14, column = 4, columnspan = 3, sticky = 'e', ipadx = 5, ipady = 5, pady = 20)

    def display_last_five(self):
        #starting row 9

        self.last_five = tk.Frame(master = self.parent)
        data = self.df.tail(5).to_numpy()
        columns = self.df.columns.tolist()

        for i, col in enumerate(columns):
            header = tk.Label(self.last_five, text = col, font = ('Verdana' , 12), borderwidth =1, relief = 'solid')
            header.grid(row = 0, column = i, sticky = 'nsew', ipadx = 10, ipady = 10)

        rows, columns = data.shape
        for i in range(rows):
            for j in range(columns):
                header = tk.Label(self.last_five, text = data[i][j], font = ('Verdana' , 12), borderwidth =1, relief = 'solid')
                header.grid(row = i+1, column = j, sticky = 'nsew')
        self.lbl_delete = tk.Label(self.parent, text = 'Last Five Transactions' , font = ('Helvetica' , 12, 'bold italic'))
        self.lbl_delete.grid(row = 9 ,column = 0, columnspan = 5, padx = 10,pady = 10, sticky ='w')
        self.last_five.grid(row = 10, column = 0, columnspan = 10, padx =10, sticky= 'w')

    def check_valid_date(day,month,year):
        total_valid_dates = 31 if month == 12 else (datetime.date(year,month + 1,1) - datetime.date(year, month,1)).days
        return day <= total_valid_dates
    
    def commit_transaction(self):
        #check all the input, debt is not allowed
        month = self.month_variable.get()
        year = self.year_variable.get()
        
        curr_date = self.day_variable.get()
        try :
            assert check_valid_date(curr_date,month,year)
        except :
            self.lbl_error['borderwidth'] = 2
            self.lbl_error['height'] = 2
            self.lbl_error['text'] = 'invalid date for month {}'.format(month)
        
        date = datetime.datetime(year,month,curr_date).date()
        trans_type = 'D' if self.trans_variable.get() == 'Deposit' else 'W'
        description = self.txt_description.get("1.0", tk.END).rstrip()
        if len(description) == 0 : #empty string
            description = '-'
            
        amount = self.ety_amount.get()
        try :
            float_amount = float(amount)
            self.append_data(date, description, trans_type, float_amount)
            self.df.to_csv('transaction.csv', index = False)
            self.df = read_data()
            self.last_five.grid_forget()
            self.display_last_five()
        except :
            self.lbl_error['borderwidth'] = 2
            self.lbl_error['height'] = 2
            self.lbl_error['text'] = 'invalid amount of {}'.format('None' if amount == '' else amount)

    def append_data(self, date, description, transaction_type, amount):
        #transaction type : 'D' deposit/ 'W' withdrawal
        last_transaction_code = int(self.df.tail(1).ID.values[0][1:]) if len(self.df) > 1 else 0
        Ref = f'{ transaction_type + str(last_transaction_code + 1)}'
        if transaction_type == 'D' :
            row = pd.Series([Ref,date, description, 0, amount, get_current_balance(self.df) + amount],
                            index = ['ID','Date','Description','Withdrawal',
                                     'Deposit','Balance'])
        else :
            row = pd.Series([Ref,date, description, amount, 0, get_current_balance(self.df) - amount],
                            index = ['ID','Date','Description','Withdrawal',
                                     'Deposit','Balance'])
        self.df = self.df.append(row, ignore_index = True)
        

        self.lbl_error['borderwidth'] = 2
        self.lbl_error['height'] = 2
        self.lbl_error['text'] = 'Transaction Successful'

        #clear data & send message
        self.clear()

    def clear(self):
        self.txt_description.delete("1.0", tk.END)
        self.ety_amount.delete("0", tk.END)

    def delete_id(self):
        refid = self.ety_refid.get()
        try :
            target_id = self.df[self.df['ID'] == refid].index.values[0].astype(int)
            self.df.drop([target_id], inplace = True)
            
            self.lbl_error['borderwidth'] = 2
            self.lbl_error['height'] = 2
            self.lbl_error['text'] = 'Transaction ID {} Deleted'.format(refid)

            self.df.to_csv('transaction.csv', index = False)
            self.df = read_data()
            self.last_five.grid_forget()
            self.display_last_five()

        except : # not found
            self.lbl_error['borderwidth'] = 2
            self.lbl_error['height'] = 2
            self.lbl_error['text'] = 'ID {} not found'.format(refid)

    def summary(self):
        df = self.df
        
        fig, ax =plt.subplots(figsize=(12,4))
        ax.axis('tight')
        ax.axis('off')
        table = ax.table(cellText = df.values, colLabels = df.columns, loc = 'center')
        table.scale(1,4)

        pp = PdfPages("full_report.pdf")
        pp.savefig(fig, bbox_inches='tight')
        pp.close()

    def partial_summary(self):

        try :
            from_date = datetime.date(self.year_variable_from.get(), self.month_variable_from.get(), self.day_variable_from.get())
            to_date = datetime.date(self.year_variable_to.get(), self.month_variable_to.get(), self.day_variable_to.get())
        except :
            self.lbl_error['borderwidth'] = 2
            self.lbl_error['height'] = 2
            self.lbl_error['text'] = 'day is out of range for month'

        from_date, to_date = pd.Timestamp(from_date), pd.Timestamp(to_date)
        
        df = self.df[1:] # ignore first item since its empty
        df = df[(from_date <= pd.to_datetime(df.Date)) & ( pd.to_datetime(df.Date)<= to_date )]
        fig, ax =plt.subplots(figsize=(12,4))
        ax.axis('tight')
        ax.axis('off')
        table = ax.table(cellText = df.values, colLabels = df.columns, loc = 'center')
        table.scale(1,4)

        pp = PdfPages("report_from_{}_to_{}.pdf".format(from_date.date(), to_date.date()))
        pp.savefig(fig, bbox_inches='tight')
        pp.close()
        
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('600x800')
    App(root).grid(row = 0, column = 0)
    root.mainloop()




