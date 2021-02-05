
# coding: utf-8

# In[ ]:


from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import pandas as pd
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
import requests
import tkinter as tk
from tkinter import *
from tkinter import ttk
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class final_project(tk.Tk):
    
    def __init__(self,*args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        
        container.pack(side="top", fill="both", expand = True)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        for F in (StartPage, CalcPage):
            frame1 = F(container, self)

            self.frames[F] = frame1

            frame1.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(StartPage)
        
    def show_frame(self, cont):
        
        frame = self.frames[cont]
        frame.tkraise()
        
def qf(param):
    print(param)
        
class StartPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page")
        label.pack(pady=10, padx=10)
        
        f = Figure()
        ax = f.add_subplot(111)
        
        fd_html = urlopen('http://api.eia.gov/series/?api_key=bdc665fdd718f4f2624518fada5e39f8&series_id=EBA.US48-ALL.DF.H')
        fd_raw = BeautifulSoup(fd_html.read(), "lxml");
        fd_raw = str(fd_raw);
        data_index = fd_raw.find("data");
        fd_raw = fd_raw[data_index + 8: -23]
        fd_raw = fd_raw.split('],[')

        fd_res = [];
        for i in range(len(fd_raw)):
            temp = '[' + fd_raw[i] + ']';
            temp_list = json.loads(temp);
            fd_res.append(temp_list);
        fdraw_df = pd.DataFrame(fd_res) 
        fd_clean = fdraw_df.rename(columns={0: 'UTC', 1:'Forecast'});
        fd_clean['UTC'] = pd.to_datetime(fd_clean['UTC'], format='%Y%m%dT%HZ')
        fd_clean = fd_clean.set_index('UTC');
        
        td_html = urlopen('http://api.eia.gov/series/?api_key=bdc665fdd718f4f2624518fada5e39f8&series_id=EBA.US48-ALL.D.H')
        td_raw = BeautifulSoup(td_html.read(), "lxml")
        td_raw = str(td_raw)
        data_index = td_raw.find("data")
        td_raw = td_raw[data_index + 8: -23]
        td_raw = td_raw.split('],[')

        td_res = [];
        for i in range(len(td_raw)):
            temp = '[' + td_raw[i] + ']';
            temp_list = json.loads(temp);
            td_res.append(temp_list);
        tdraw_df = pd.DataFrame(td_res)
        td_clean = tdraw_df.rename(columns={0: 'UTC', 1:'TotalDemand'});

        td_clean['UTC'] = pd.to_datetime(td_clean['UTC'], format='%Y%m%dT%HZ')
        td_clean = td_clean.set_index('UTC')
        
        tg_html = urlopen('http://api.eia.gov/series/?api_key=bdc665fdd718f4f2624518fada5e39f8&series_id=EBA.US48-ALL.NG.H')
        tg_raw = BeautifulSoup(tg_html.read(), "lxml")
        tg_raw = str(tg_raw)
        data_index = tg_raw.find("data")
        tg_raw = tg_raw[data_index + 8: -23]
        tg_raw = tg_raw.split('],[')
        res = [];
        for i in range(len(tg_raw)):
            temp = '[' + tg_raw[i] + ']';
            temp_list = json.loads(temp);
            res.append(temp_list);
        tgraw_df = pd.DataFrame(res) 
        tg_clean = tgraw_df.rename(columns={0: 'UTC', 1:'TotalGeneration'});
        tg_clean['UTC'] = pd.to_datetime(tg_clean['UTC'], format='%Y%m%dT%HZ')
        tg_clean = tg_clean.set_index('UTC')
        
        fd_clean = fd_clean.head(400)
        td_clean = td_clean.head(400)
        tg_clean = tg_clean.head(400)
        
        ax.plot(fd_clean, label="Forecast Demand")
        td_clean.plot(ax=ax, label="Total Demand")
        tg_clean.plot(ax=ax, label="Total Gen")
        ax.legend()
        
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        f1 = Figure()
        ax1 = f1.add_subplot(211)
        ax2 = f1.add_subplot(212)
        
        datelist = pd.date_range(pd.datetime.today(), periods=10,  freq='D').date.tolist()
        
        html = urlopen('https://markets.businessinsider.com/commodities/oil-price?type=wti')
        wtioil=BeautifulSoup(html.read(), "lxml")

        wti_table_list=wtioil.findAll('td',{ "class" : "text-right" })
        wti_history=[]

        for i in range(0, 40, 4):
            for wti in wti_table_list[i].children:
                wti_history.append(str(wti).replace('\t','').replace('\r','').replace('\n',''))

        ax1.plot(datelist, wti_history)
        ax1.set_title("wti history")
        
        html = urlopen('https://markets.businessinsider.com/commodities/natural-gas-price')
        his_gas=BeautifulSoup(html.read(), "lxml")

        hisgas_table_list=his_gas.findAll('td',
                              { "class" : "text-right" } )

        gas_history=[]

        for i in range(0, 40, 4):
            for hisgas in hisgas_table_list[i].children:
                gas_history.append(str(hisgas).replace('\t','').replace('\r','').replace('\n',''))

        ax2.plot(datelist, gas_history)
        ax2.set_title("gas history")
       
        canvas1 = FigureCanvasTkAgg(f1, self)
        canvas1.draw()
        canvas1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        button1 = ttk.Button(self, text="Calculate Price", 
                            command=lambda: controller.show_frame(CalcPage))
        button1.pack()
        
class CalcPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Calc Page")
        label.pack(pady=10, padx=10)
        
        e = Entry(self, width=25)
        e.pack()
        
        def callback():
            
            invest_amt = int(e.get())
            
            fd_html = urlopen('http://api.eia.gov/series/?api_key=bdc665fdd718f4f2624518fada5e39f8&series_id=EBA.US48-ALL.DF.H')
            fd_raw = BeautifulSoup(fd_html.read(), "lxml");
            fd_raw = str(fd_raw);
            data_index = fd_raw.find("data");
            fd_raw = fd_raw[data_index + 8: -23]
            fd_raw = fd_raw.split('],[')

            fd_res = [];
            for i in range(len(fd_raw)):
                temp = '[' + fd_raw[i] + ']';
                temp_list = json.loads(temp);
                fd_res.append(temp_list);
            fdraw_df = pd.DataFrame(fd_res) 
            fd_clean = fdraw_df.rename(columns={0: 'UTC', 1:'Forecast'});
            fd_clean['UTC'] = pd.to_datetime(fd_clean['UTC'], format='%Y%m%dT%HZ')
            fd_clean = fd_clean.set_index('UTC');

            td_html = urlopen('http://api.eia.gov/series/?api_key=bdc665fdd718f4f2624518fada5e39f8&series_id=EBA.US48-ALL.D.H')
            td_raw = BeautifulSoup(td_html.read(), "lxml")
            td_raw = str(td_raw)
            data_index = td_raw.find("data")
            td_raw = td_raw[data_index + 8: -23]
            td_raw = td_raw.split('],[')

            td_res = [];
            for i in range(len(td_raw)):
                temp = '[' + td_raw[i] + ']';
                temp_list = json.loads(temp);
                td_res.append(temp_list);
            tdraw_df = pd.DataFrame(td_res)
            td_clean = tdraw_df.rename(columns={0: 'UTC', 1:'TotalDemand'});

            td_clean['UTC'] = pd.to_datetime(td_clean['UTC'], format='%Y%m%dT%HZ')
            td_clean = td_clean.set_index('UTC')

            tg_html = urlopen('http://api.eia.gov/series/?api_key=bdc665fdd718f4f2624518fada5e39f8&series_id=EBA.US48-ALL.NG.H')
            tg_raw = BeautifulSoup(tg_html.read(), "lxml")
            tg_raw = str(tg_raw)
            data_index = tg_raw.find("data")
            tg_raw = tg_raw[data_index + 8: -23]
            tg_raw = tg_raw.split('],[')
            res = [];
            for i in range(len(tg_raw)):
                temp = '[' + tg_raw[i] + ']';
                temp_list = json.loads(temp);
                res.append(temp_list);
            tgraw_df = pd.DataFrame(res) 
            tg_clean = tgraw_df.rename(columns={0: 'UTC', 1:'TotalGeneration'});
            tg_clean['UTC'] = pd.to_datetime(tg_clean['UTC'], format='%Y%m%dT%HZ')
            tg_clean = tg_clean.set_index('UTC')

            current_time = str(tg_clean.index[0])

            html = urlopen('https://markets.businessinsider.com/commodities/natural-gas-price')
            bgas = BeautifulSoup(html.read(), "lxml")
            gas_table_list = bgas.findAll('span',
                                  { "class" : "push-data" } )
            gas_table=gas_table_list[0]
            for gas in gas_table.children:
                live_price_gas = float(gas)
                
            html = urlopen('https://markets.businessinsider.com/commodities/oil-price?type=wti')
            boil= BeautifulSoup(html.read(), "lxml")
            oil_table_list = boil.findAll('span',
                                  { "class" : "push-data" } )
            oil_table=oil_table_list[0]
            for oil in oil_table.children:
                live_price_oil=float(oil)

            response = requests.get("https://api.eia.gov/series/?api_key=bdc665fdd718f4f2624518fada5e39f8&series_id=EBA.US48-ALL.NG.OIL.H")
            raw_data = json.loads(response.text)
            temp_list = raw_data['series'][0]['data']
            temp_df = pd.DataFrame(temp_list)
            temp_df = temp_df.rename(columns={0: 'UTC', 1:'Gen'});
            temp_df['UTC'] = pd.to_datetime(temp_df['UTC'], format='%Y%m%dT%HZ')

            index = temp_df.index[temp_df['UTC'] == current_time];
            '''
            Essentially the first element in the list will represent the recent most current date.
            Hence taking the value for that and subtracting it with the 6th element
            '''
            change = int(temp_df.loc[index+5]['Gen']) - int(temp_df.loc[index + 10]['Gen'])

            #if change is negative put 0
            if change > 0:
                changerPerForOil = change/float(temp_df.loc[index+5]['Gen'])
            else:
                changerPerForOil = 0

            #API for Natural gas, repeat similar steps as for oil
            response = requests.get("http://api.eia.gov/series/?api_key=bdc665fdd718f4f2624518fada5e39f8&series_id=EBA.US48-ALL.NG.NG.H")
            raw_data = json.loads(response.text)
            temp_list = raw_data['series'][0]['data']

            temp_df = pd.DataFrame(temp_list)
            temp_df = temp_df.rename(columns={0: 'UTC', 1:'Gen'});
            temp_df['UTC'] = pd.to_datetime(temp_df['UTC'], format='%Y%m%dT%HZ')

            index = temp_df.index[temp_df['UTC'] == current_time];
            change = int(temp_df.loc[index+5]['Gen']) - int(temp_df.loc[index + 10]['Gen'])

            if change > 0:
                changerPerForNG = change/float(temp_df.loc[index+5]['Gen'])
            else:
                changerPerForNG = 0

            data = {'Type':['Oil', 'Natural Gas'],
                    '% Change':[changerPerForOil,changerPerForNG ]} 

            gen_df = pd.DataFrame(data)
            print(gen_df)
            print(tg_clean.iloc[0].TotalGeneration)
            c_time = pd.Timestamp.utcnow()- pd.offsets.Hour(1);
            c_time = c_time.strftime('%Y-%m-%d %H:00:00');

            comp_df = pd.DataFrame(fd_clean[:current_time])
            print(comp_df)
            comp_df['change Demand'] = 100 * (comp_df.Forecast - float(tg_clean.loc[current_time].TotalGeneration))/(float(tg_clean.loc[current_time].TotalGeneration))
            comp_df.loc[comp_df['change Demand'] < 0, 'change Demand'] = 0
            comp_df['Change Oil'] = (gen_df.loc[0]['% Change'] * comp_df['change Demand']);
            comp_df['Change Gas'] = (gen_df.loc[1]['% Change'] * comp_df['change Demand']);

            comp_df['final_oil'] = ((100+comp_df['Change Oil']) * invest_amt)/100
            comp_df['final_gas'] = ((100+comp_df['Change Gas']) * invest_amt)/100

            comp_df = comp_df.drop(['Change Oil','Change Gas', 'change Demand'], axis=1)
            
            lbl1.set('Live oil price: ' + str(live_price_oil));
            lbl2.set('Live gas price: ' + str(live_price_gas))
            lbl3.set('Current time(UTC)'': ' + str(c_time))
            lbl4.set(comp_df.to_string())

        
        lbl1 = tk.StringVar()
        lbl1.set('waiting for price')
        tk.Label(self, textvariable=lbl1).pack()
        
        lbl2 = tk.StringVar()
        lbl2.set('')
        tk.Label(self, textvariable=lbl2).pack()
        
        lbl3 = tk.StringVar()
        lbl3.set('')
        tk.Label(self, textvariable=lbl3).pack()
        
        lbl4 = tk.StringVar()
        lbl4.set('')
        tk.Label(self, textvariable=lbl4, width=300).pack()
        
        b = Button(self, text="get price", width=10, command=callback)
        b.pack()
        
        button1 = ttk.Button(self, text="Go back", 
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()
        
app = final_project()
app.mainloop()
        

