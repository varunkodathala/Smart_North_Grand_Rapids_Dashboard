
import streamlit as st
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def check_threshold(data, dates, vehicle_category):

  content = f'Exceeded Flow of {vehicle_category}:'
  threshold = sum(data)//len(data)
  for i in range(len(data)):
    if data[i]>threshold:
      content += f'\nDate:{dates[i]} Total Number of Vehicles: {data[i]} Target Set: {threshold} Deviation: {abs(data[i]-threshold)}'
  return content

def send_email(user,email,data, dates, vehicle_category):

  
  mail_content = f'''Hello {user},
  
System detected multiple outliers which are greater than the threshold at following incidents:'''
  mail_content+='\n'

  mail_content+= check_threshold(data, dates, vehicle_category)

  mail_content += '\n\nThank you \nTeam Vizworld'

  sender_address = 'grvizworldalerts@gmail.com'
  sender_pass = 'hwwokgwxrsoaoutq'
  receiver_address = email

  message = MIMEMultipart()
  message['From'] = sender_address
  message['To'] = receiver_address
  message['Subject'] = f'Traffic Alert'

  message.attach(MIMEText(mail_content, 'plain'))
  session = smtplib.SMTP('smtp.gmail.com', 587)
  session.starttls()
  
  session.login(sender_address, sender_pass)
  text = message.as_string()
  session.sendmail(sender_address, receiver_address, text)
  session.quit()



st.set_page_config(page_title='Smart North - Traffic Analysis Dashboard',  layout='wide', page_icon=':car:')

#this is the header
 

t1, t2, t3 = st.columns((0.07,1,0.07)) 

t1.image('images\Smart_North_Vertical_2Color-686x1024.png', width = 120)
t2.markdown("<h2 style='text-align: center; color: navy; font-family: 'Trebuchet MS', sans-serif;'>Traffic and Mobility Analysis at Grand Rapids, MN</h2>", unsafe_allow_html=True)
t2.markdown("<h3 style='text-align: center; color: black; font-family: 'Trebuchet MS', sans-serif;'>Powered by Vizworld Inc.</h3>", unsafe_allow_html=True)
t3.image('images/viz.jpg', width = 120)

report_range = st.selectbox('Choose Range', ['09/24/2022 to 10/07/2022','10/08/2022 to 10/21/2022','10/22/2022 to 11/04/2022','09/24/2022 to 11/04/2022'])

## Data

with st.spinner('Updating Report...'):
    
    if '09/24/2022 to 10/07/2022' == report_range:
        g1, g2, g3 = st.columns((1,1,1))

        # Graph 1 - SV
        df = pd.read_csv('data/final_comprehensive_data.csv')
        y1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        dates_idx = list(range(1,15))

        y1_count = 0
        y2_count = 0
        y3_count = 0

        for id in dates_idx:
            for i in range(len(df)):
                if df['dates_ids'][i] == id:
                    if df['Vehicle Type'][i] == 'small_vehicle':
                        y1_count += df['Count'][i]
                    elif df['Vehicle Type'][i] == 'bus':
                        y2_count += df['Count'][i]
                    else:
                        y3_count += df['Count'][i]
            y1[dates_idx.index(id)] = y1_count
            y2[dates_idx.index(id)] = y2_count
            y3[dates_idx.index(id)] = y3_count
            y1_count = 0
            y2_count = 0
            y3_count = 0
        
        dates = ['09/24','09/25','09/26','09/27','09/28','09/29','09/30','10/01','10/02','10/03','10/04','10/05','10/06','10/07']

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=y1,
            name='Small Vehicles',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=dates, y=[sum(y1)//len(y1) for i in range(1,15)], mode='lines', line=dict(color="black"), name='Target')
        fig.update_layout(title_text="Flow of Small Vehicles",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g1.plotly_chart(fig, use_container_width=True) 
        
        small_vehicles_data = y1
        # Graph 2 - Buses
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=y2,
            name='Buses',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=dates, y=[sum(y2)//len(y2) for i in range(1,15)], mode='lines', line=dict(color="black"), name='Target')
        fig.update_layout(title_text="Flow of Buses",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))       
        g2.plotly_chart(fig, use_container_width=True) 

        buses_data = y2
        # Graph 3 - LV
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=y3,
            name='Large Vehicles',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=dates, y=[sum(y3)//len(y3) for i in range(1,15)], mode='lines', line=dict(color="black"), name='Target')
        fig.update_layout(title_text="Flow of Large Vehicles",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))       
        g3.plotly_chart(fig, use_container_width=True) 

        large_vehicles_data = y3

        # Graph 4 - Pole 1: SV

        y1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        dates_idx = list(range(1,15))

        y1_count = 0
        y2_count = 0
        y3_count = 0

        for id in dates_idx:
            for i in range(len(df)):
                if df['dates_ids'][i] == id and df['poles_ids'][i] == 1:
                    if df['Vehicle Type'][i] == 'small_vehicle':
                        y1_count += df['Count'][i]
                    elif df['Vehicle Type'][i] == 'bus':
                        y2_count += df['Count'][i]
                    else:
                        y3_count += df['Count'][i]
            y1[dates_idx.index(id)] = y1_count
            y2[dates_idx.index(id)] = y2_count
            y3[dates_idx.index(id)] = y3_count
            y1_count = 0
            y2_count = 0
            y3_count = 0
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=y1,
            name='Small Vehicles',
            marker_color='lightseagreen'
        ))
        fig.add_scatter(x=dates, y=[sum(y1)//len(y1) for i in range(1,15)], mode='lines', line=dict(color="black"), name='Target')
        fig.update_layout(title_text="Flow of Small Vehicles across pole 1",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g1.plotly_chart(fig, use_container_width=True) 
        
        # Graph 2 - Pole 1: Buses
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=y2,
            name='Buses',
            marker_color='lightseagreen'
        ))
        fig.add_scatter(x=dates, y=[sum(y2)//len(y2) for i in range(1,15)], mode='lines', line=dict(color="black"), name='Target')
        fig.update_layout(title_text="Flow of Buses across pole 1",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))       
        g2.plotly_chart(fig, use_container_width=True) 

        # Graph 3 - Pole 1: LV
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=y3,
            name='Large Vehicles',
            marker_color='lightseagreen'
        ))
        fig.add_scatter(x=dates, y=[sum(y3)//len(y3) for i in range(1,15)], mode='lines', line=dict(color="black"), name='Target')
        fig.update_layout(title_text="Flow of Large Vehicles across pole 1",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))       
        g3.plotly_chart(fig, use_container_width=True) 


        # Graph 4 - Pole 2: SV

        y1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        dates_idx = list(range(1,15))

        y1_count = 0
        y2_count = 0
        y3_count = 0

        for id in dates_idx:
            for i in range(len(df)):
                if df['dates_ids'][i] == id and df['poles_ids'][i] == 2:
                    if df['Vehicle Type'][i] == 'small_vehicle':
                        y1_count += df['Count'][i]
                    elif df['Vehicle Type'][i] == 'bus':
                        y2_count += df['Count'][i]
                    else:
                        y3_count += df['Count'][i]
            y1[dates_idx.index(id)] = y1_count
            y2[dates_idx.index(id)] = y2_count
            y3[dates_idx.index(id)] = y3_count
            y1_count = 0
            y2_count = 0
            y3_count = 0
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=y1,
            name='Small Vehicles',
            marker_color='lightcoral'
        ))
        fig.add_scatter(x=dates, y=[sum(y1)//len(y1) for i in range(1,15)], mode='lines', line=dict(color="black"), name='Target')
        fig.update_layout(title_text="Flow of Small Vehicles across pole 2",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g1.plotly_chart(fig, use_container_width=True) 
        
        # Graph 2 - Pole 2: Buses
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=y2,
            name='Buses',
            marker_color='lightcoral'
        ))
        fig.add_scatter(x=dates, y=[sum(y2)//len(y2) for i in range(1,15)], mode='lines', line=dict(color="black"), name='Target')
        fig.update_layout(title_text="Flow of Buses across pole 2",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))       
        g2.plotly_chart(fig, use_container_width=True) 

        # Graph 3 - Pole 2: LV
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=y3,
            name='Large Vehicles',
            marker_color='lightcoral'
        ))
        fig.add_scatter(x=dates, y=[sum(y3)//len(y3) for i in range(1,15)], mode='lines', line=dict(color="black"), name='Target')
        fig.update_layout(title_text="Flow of Large Vehicles across pole 2",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))       
        g3.plotly_chart(fig, use_container_width=True) 

    # Graph 4 - Pole 3: SV

        y1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        dates_idx = list(range(1,15))

        y1_count = 0
        y2_count = 0
        y3_count = 0

        for id in dates_idx:
            for i in range(len(df)):
                if df['dates_ids'][i] == id and df['poles_ids'][i] == 3:
                    if df['Vehicle Type'][i] == 'small_vehicle':
                        y1_count += df['Count'][i]
                    elif df['Vehicle Type'][i] == 'bus':
                        y2_count += df['Count'][i]
                    else:
                        y3_count += df['Count'][i]
            y1[dates_idx.index(id)] = y1_count
            y2[dates_idx.index(id)] = y2_count
            y3[dates_idx.index(id)] = y3_count
            y1_count = 0
            y2_count = 0
            y3_count = 0
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=y1,
            name='Small Vehicles',
            marker_color='lightsalmon'
        ))
        fig.add_scatter(x=dates, y=[sum(y1)//len(y1) for i in range(1,15)], mode='lines', line=dict(color="black"), name='Target')
        fig.update_layout(title_text="Flow of Small Vehicles across pole 3",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g1.plotly_chart(fig, use_container_width=True) 
        
        # Graph 2 - Pole 3: Buses
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=y2,
            name='Buses',
            marker_color='lightsalmon'
        ))
        fig.add_scatter(x=dates, y=[sum(y2)//len(y2) for i in range(1,15)], mode='lines', line=dict(color="black"), name='Target')
        fig.update_layout(title_text="Flow of Buses across pole 3",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))       
        g2.plotly_chart(fig, use_container_width=True) 

        # Graph 3 - Pole 3: LV
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=y3,
            name='Large Vehicles',
            marker_color='lightsalmon'
        ))
        fig.add_scatter(x=dates, y=[sum(y3)//len(y3) for i in range(1,15)], mode='lines', line=dict(color="black"), name='Target')
        fig.update_layout(title_text="Flow of Large Vehicles across pole 3",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))       
        g3.plotly_chart(fig, use_container_width=True) 

        g1,g2 = st.columns((1,1))    

        y1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        times_idx = list(range(0,24))

        y1_count = 0
        y2_count = 0
        y3_count = 0

        for id in times_idx:
            for i in range(len(df)):
                if int(df['times'][i]) == id and df['dates_ids'][i] >= 1 and df['dates_ids'][i] <= 14:
                    if df['Vehicle Type'][i] == 'small_vehicle':
                        y1_count += df['Count'][i]
                    elif df['Vehicle Type'][i]  == 'bus':
                        y2_count += df['Count'][i]
                    else:
                        y3_count += df['Count'][i]
            y1[times_idx.index(id)] = y1_count
            y2[times_idx.index(id)] = y2_count
            y3[times_idx.index(id)] = y3_count
            y1_count = 0
            y2_count = 0
            y3_count = 0
        
        times = ['0:00 AM','1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM']

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y1,
            name='Small Vehicles',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y1)//len(y1) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of Small Vehicles",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g1.plotly_chart(fig, use_container_width=True) 

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y2,
            name='Buses',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y2)//len(y2) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of Buses",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g2.plotly_chart(fig, use_container_width=True) 

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y3,
            name='Large Vehicles',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y3)//len(y3) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of Large Vehicles",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g1.plotly_chart(fig, use_container_width=True) 

        y1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        times_idx = list(range(0,24))

        y1_count = 0
        y2_count = 0
        y3_count = 0

        for id in times_idx:
            for i in range(len(df)):
                if int(df['times'][i]) == id and df['dates_ids'][i] >= 1 and df['dates_ids'][i] <= 14 and df['poles_ids'][i] == 1:
                    if df['Vehicle Type'][i] == 'small_vehicle':
                        y1_count += df['Count'][i]
                    elif df['Vehicle Type'][i]  == 'bus':
                        y2_count += df['Count'][i]
                    else:
                        y3_count += df['Count'][i]
            y1[times_idx.index(id)] = y1_count
            y2[times_idx.index(id)] = y2_count
            y3[times_idx.index(id)] = y3_count
            y1_count = 0
            y2_count = 0
            y3_count = 0
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y1,
            name='Small Vehicles',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y1)//len(y1) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of Small Vehicles across pole 1",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g2.plotly_chart(fig, use_container_width=True) 

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y2,
            name='Buses',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y2)//len(y2) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of Buses across pole 1",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g1.plotly_chart(fig, use_container_width=True) 

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y3,
            name='Large Vehicles',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y3)//len(y3) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of Large Vehicles across pole 1",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g2.plotly_chart(fig, use_container_width=True) 

        y1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        times_idx = list(range(0,24))

        y1_count = 0
        y2_count = 0
        y3_count = 0

        for id in times_idx:
            for i in range(len(df)):
                if int(df['times'][i]) == id and df['dates_ids'][i] >= 1 and df['dates_ids'][i] <= 14 and df['poles_ids'][i] == 2:
                    if df['Vehicle Type'][i] == 'small_vehicle':
                        y1_count += df['Count'][i]
                    elif df['Vehicle Type'][i]  == 'bus':
                        y2_count += df['Count'][i]
                    else:
                        y3_count += df['Count'][i]
            y1[times_idx.index(id)] = y1_count
            y2[times_idx.index(id)] = y2_count
            y3[times_idx.index(id)] = y3_count
            y1_count = 0
            y2_count = 0
            y3_count = 0
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y1,
            name='Small Vehicles',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y1)//len(y1) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of Small Vehicles across pole 2",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g1.plotly_chart(fig, use_container_width=True) 

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y2,
            name='Buses',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y2)//len(y2) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of Buses across pole 2",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g2.plotly_chart(fig, use_container_width=True) 

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y3,
            name='Large Vehicles',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y3)//len(y3) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of Large Vehicles across pole 2",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g1.plotly_chart(fig, use_container_width=True) 

        y1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        times_idx = list(range(0,24))

        y1_count = 0
        y2_count = 0
        y3_count = 0

        for id in times_idx:
            for i in range(len(df)):
                if int(df['times'][i]) == id and df['dates_ids'][i] >= 1 and df['dates_ids'][i] <= 14 and df['poles_ids'][i] == 3:
                    if df['Vehicle Type'][i] == 'small_vehicle':
                        y1_count += df['Count'][i]
                    elif df['Vehicle Type'][i]  == 'bus':
                        y2_count += df['Count'][i]
                    else:
                        y3_count += df['Count'][i]
            y1[times_idx.index(id)] = y1_count
            y2[times_idx.index(id)] = y2_count
            y3[times_idx.index(id)] = y3_count
            y1_count = 0
            y2_count = 0
            y3_count = 0

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y1,
            name='Small Vehicles',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y1)//len(y1) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of Small Vehicles across pole 3",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g2.plotly_chart(fig, use_container_width=True) 

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y2,
            name='Buses',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y2)//len(y2) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of Buses across pole 3",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g1.plotly_chart(fig, use_container_width=True) 

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y3,
            name='Large Vehicles',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y3)//len(y3) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of Large Vehicles across pole 3",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g2.plotly_chart(fig, use_container_width=True) 

        y1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        times_idx = list(range(0,24))

        y1_count = 0

        for id in times_idx:
            for i in range(len(df)):
                if int(df['times'][i]) == id and df['dates_ids'][i] >= 1 and df['dates_ids'][i] <= 14:
                    y1_count += df['Count'][i]
            y1[times_idx.index(id)] = y1_count
            y1_count = 0


        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y1,
            name='All Vehicles',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y1)//len(y1) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of All Vehicles",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        st.plotly_chart(fig, use_container_width=True)
        with st.form("my_form"):
            st.write("")
            Name = st.text_input('Name')
            Email = st.text_input('Email')
            submitted = st.form_submit_button("Send Alerts!")
            if submitted:
                send_email(Name,Email,small_vehicles_data, dates, 'Small Vehicles')
                send_email(Name,Email,buses_data, dates, 'Buses')
                send_email(Name,Email,large_vehicles_data, dates, 'Large Vehicles')

    elif '10/08/2022 to 10/21/2022' == report_range:
        g1, g2, g3 = st.columns((1,1,1))

        # Graph 1 - SV
        df = pd.read_csv('data/final_comprehensive_data.csv')
        y1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        dates_idx = list(range(15,29))

        y1_count = 0
        y2_count = 0
        y3_count = 0

        for id in dates_idx:
            for i in range(len(df)):
                if df['dates_ids'][i] == id:
                    if df['Vehicle Type'][i] == 'small_vehicle':
                        y1_count += df['Count'][i]
                    elif df['Vehicle Type'][i] == 'bus':
                        y2_count += df['Count'][i]
                    else:
                        y3_count += df['Count'][i]
            y1[dates_idx.index(id)] = y1_count
            y2[dates_idx.index(id)] = y2_count
            y3[dates_idx.index(id)] = y3_count
            y1_count = 0
            y2_count = 0
            y3_count = 0
        
        dates = ['10/08','10/09','10/10','10/11','10/12','10/13','10/14','10/15','10/16','10/17','10/18','10/19','10/20','10/21']

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=y1,
            name='Small Vehicles',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=dates, y=[sum(y1)//len(y1) for i in range(1,15)], mode='lines', line=dict(color="black"), name='Target')
        fig.update_layout(title_text="Flow of Small Vehicles",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g1.plotly_chart(fig, use_container_width=True) 
        
        small_vehicles_data = y1

        # Graph 2 - Buses
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=y2,
            name='Buses',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=dates, y=[sum(y2)//len(y2) for i in range(1,15)], mode='lines', line=dict(color="black"), name='Target')
        fig.update_layout(title_text="Flow of Buses",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))       
        g2.plotly_chart(fig, use_container_width=True) 

        buses_data = y2
        # Graph 3 - LV
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=y3,
            name='Large Vehicles',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=dates, y=[sum(y3)//len(y3) for i in range(1,15)], mode='lines', line=dict(color="black"), name='Target')
        fig.update_layout(title_text="Flow of Large Vehicles",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))       
        g3.plotly_chart(fig, use_container_width=True) 

        large_vehicles_data = y3
        # Graph 4 - Pole 1: SV

        y1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        dates_idx = list(range(15,29))

        y1_count = 0
        y2_count = 0
        y3_count = 0

        for id in dates_idx:
            for i in range(len(df)):
                if df['dates_ids'][i] == id and df['poles_ids'][i] == 1:
                    if df['Vehicle Type'][i] == 'small_vehicle':
                        y1_count += df['Count'][i]
                    elif df['Vehicle Type'][i] == 'bus':
                        y2_count += df['Count'][i]
                    else:
                        y3_count += df['Count'][i]
            y1[dates_idx.index(id)] = y1_count
            y2[dates_idx.index(id)] = y2_count
            y3[dates_idx.index(id)] = y3_count
            y1_count = 0
            y2_count = 0
            y3_count = 0
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=y1,
            name='Small Vehicles',
            marker_color='lightseagreen'
        ))
        fig.add_scatter(x=dates, y=[sum(y1)//len(y1) for i in range(1,15)], mode='lines', line=dict(color="black"), name='Target')
        fig.update_layout(title_text="Flow of Small Vehicles across pole 1",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g1.plotly_chart(fig, use_container_width=True) 
        
        # Graph 2 - Pole 1: Buses
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=y2,
            name='Buses',
            marker_color='lightseagreen'
        ))
        fig.add_scatter(x=dates, y=[sum(y2)//len(y2) for i in range(1,15)], mode='lines', line=dict(color="black"), name='Target')
        fig.update_layout(title_text="Flow of Buses across pole 1",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))       
        g2.plotly_chart(fig, use_container_width=True) 

        # Graph 3 - Pole 1: LV
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=y3,
            name='Large Vehicles',
            marker_color='lightseagreen'
        ))
        fig.add_scatter(x=dates, y=[sum(y3)//len(y3) for i in range(1,15)], mode='lines', line=dict(color="black"), name='Target')
        fig.update_layout(title_text="Flow of Large Vehicles across pole 1",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))       
        g3.plotly_chart(fig, use_container_width=True) 


        # Graph 4 - Pole 2: SV

        y1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        dates_idx = list(range(15,29))

        y1_count = 0
        y2_count = 0
        y3_count = 0

        for id in dates_idx:
            for i in range(len(df)):
                if df['dates_ids'][i] == id and df['poles_ids'][i] == 2:
                    if df['Vehicle Type'][i] == 'small_vehicle':
                        y1_count += df['Count'][i]
                    elif df['Vehicle Type'][i] == 'bus':
                        y2_count += df['Count'][i]
                    else:
                        y3_count += df['Count'][i]
            y1[dates_idx.index(id)] = y1_count
            y2[dates_idx.index(id)] = y2_count
            y3[dates_idx.index(id)] = y3_count
            y1_count = 0
            y2_count = 0
            y3_count = 0
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=y1,
            name='Small Vehicles',
            marker_color='lightcoral'
        ))
        fig.add_scatter(x=dates, y=[sum(y1)//len(y1) for i in range(1,15)], mode='lines', line=dict(color="black"), name='Target')
        fig.update_layout(title_text="Flow of Small Vehicles across pole 2",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g1.plotly_chart(fig, use_container_width=True) 
        
        # Graph 2 - Pole 2: Buses
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=y2,
            name='Buses',
            marker_color='lightcoral'
        ))
        fig.add_scatter(x=dates, y=[sum(y2)//len(y2) for i in range(1,15)], mode='lines', line=dict(color="black"), name='Target')
        fig.update_layout(title_text="Flow of Buses across pole 2",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))       
        g2.plotly_chart(fig, use_container_width=True) 

        # Graph 3 - Pole 2: LV
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=y3,
            name='Large Vehicles',
            marker_color='lightcoral'
        ))
        fig.add_scatter(x=dates, y=[sum(y3)//len(y3) for i in range(1,15)], mode='lines', line=dict(color="black"), name='Target')
        fig.update_layout(title_text="Flow of Large Vehicles across pole 2",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))       
        g3.plotly_chart(fig, use_container_width=True) 

    # Graph 4 - Pole 3: SV

        y1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        dates_idx = list(range(15,29))

        y1_count = 0
        y2_count = 0
        y3_count = 0

        for id in dates_idx:
            for i in range(len(df)):
                if df['dates_ids'][i] == id and df['poles_ids'][i] == 3:
                    if df['Vehicle Type'][i] == 'small_vehicle':
                        y1_count += df['Count'][i]
                    elif df['Vehicle Type'][i] == 'bus':
                        y2_count += df['Count'][i]
                    else:
                        y3_count += df['Count'][i]
            y1[dates_idx.index(id)] = y1_count
            y2[dates_idx.index(id)] = y2_count
            y3[dates_idx.index(id)] = y3_count
            y1_count = 0
            y2_count = 0
            y3_count = 0
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=y1,
            name='Small Vehicles',
            marker_color='lightsalmon'
        ))
        fig.add_scatter(x=dates, y=[sum(y1)//len(y1) for i in range(1,15)], mode='lines', line=dict(color="black"), name='Target')
        fig.update_layout(title_text="Flow of Small Vehicles across pole 3",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g1.plotly_chart(fig, use_container_width=True) 
        
        # Graph 2 - Pole 3: Buses
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=y2,
            name='Buses',
            marker_color='lightsalmon'
        ))
        fig.add_scatter(x=dates, y=[sum(y2)//len(y2) for i in range(1,15)], mode='lines', line=dict(color="black"), name='Target')
        fig.update_layout(title_text="Flow of Buses across pole 3",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))       
        g2.plotly_chart(fig, use_container_width=True) 

        # Graph 3 - Pole 3: LV
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=y3,
            name='Large Vehicles',
            marker_color='lightsalmon'
        ))
        fig.add_scatter(x=dates, y=[sum(y3)//len(y3) for i in range(1,15)], mode='lines', line=dict(color="black"), name='Target')
        fig.update_layout(title_text="Flow of Large Vehicles across pole 3",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))       
        g3.plotly_chart(fig, use_container_width=True) 

        g1,g2 = st.columns((1,1))    

        y1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        times_idx = list(range(0,24))

        y1_count = 0
        y2_count = 0
        y3_count = 0

        for id in times_idx:
            for i in range(len(df)):
                if int(df['times'][i]) == id and df['dates_ids'][i] >= 15 and df['dates_ids'][i] <= 28:
                    if df['Vehicle Type'][i] == 'small_vehicle':
                        y1_count += df['Count'][i]
                    elif df['Vehicle Type'][i]  == 'bus':
                        y2_count += df['Count'][i]
                    else:
                        y3_count += df['Count'][i]
            y1[times_idx.index(id)] = y1_count
            y2[times_idx.index(id)] = y2_count
            y3[times_idx.index(id)] = y3_count
            y1_count = 0
            y2_count = 0
            y3_count = 0
        
        times = ['0:00 AM','1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM']

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y1,
            name='Small Vehicles',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y1)//len(y1) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of Small Vehicles",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g1.plotly_chart(fig, use_container_width=True) 

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y2,
            name='Buses',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y2)//len(y2) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of Buses",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g2.plotly_chart(fig, use_container_width=True) 

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y3,
            name='Large Vehicles',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y3)//len(y3) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of Large Vehicles",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g1.plotly_chart(fig, use_container_width=True) 

        y1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        times_idx = list(range(0,24))

        y1_count = 0
        y2_count = 0
        y3_count = 0

        for id in times_idx:
            for i in range(len(df)):
                if int(df['times'][i]) == id and df['dates_ids'][i] >= 15 and df['dates_ids'][i] <= 28 and df['poles_ids'][i] == 1:
                    if df['Vehicle Type'][i] == 'small_vehicle':
                        y1_count += df['Count'][i]
                    elif df['Vehicle Type'][i]  == 'bus':
                        y2_count += df['Count'][i]
                    else:
                        y3_count += df['Count'][i]
            y1[times_idx.index(id)] = y1_count
            y2[times_idx.index(id)] = y2_count
            y3[times_idx.index(id)] = y3_count
            y1_count = 0
            y2_count = 0
            y3_count = 0
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y1,
            name='Small Vehicles',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y1)//len(y1) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of Small Vehicles across pole 1",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g2.plotly_chart(fig, use_container_width=True) 

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y2,
            name='Buses',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y2)//len(y2) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of Buses across pole 1",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g1.plotly_chart(fig, use_container_width=True) 

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y3,
            name='Large Vehicles',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y3)//len(y3) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of Large Vehicles across pole 1",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g2.plotly_chart(fig, use_container_width=True) 

        y1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        times_idx = list(range(0,24))

        y1_count = 0
        y2_count = 0
        y3_count = 0

        for id in times_idx:
            for i in range(len(df)):
                if int(df['times'][i]) == id and df['dates_ids'][i] >= 15 and df['dates_ids'][i] <= 28 and df['poles_ids'][i] == 2:
                    if df['Vehicle Type'][i] == 'small_vehicle':
                        y1_count += df['Count'][i]
                    elif df['Vehicle Type'][i]  == 'bus':
                        y2_count += df['Count'][i]
                    else:
                        y3_count += df['Count'][i]
            y1[times_idx.index(id)] = y1_count
            y2[times_idx.index(id)] = y2_count
            y3[times_idx.index(id)] = y3_count
            y1_count = 0
            y2_count = 0
            y3_count = 0
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y1,
            name='Small Vehicles',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y1)//len(y1) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of Small Vehicles across pole 2",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g1.plotly_chart(fig, use_container_width=True) 

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y2,
            name='Buses',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y2)//len(y2) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of Buses across pole 2",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g2.plotly_chart(fig, use_container_width=True) 

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y3,
            name='Large Vehicles',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y3)//len(y3) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of Large Vehicles across pole 2",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g1.plotly_chart(fig, use_container_width=True) 

        y1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        times_idx = list(range(0,24))

        y1_count = 0
        y2_count = 0
        y3_count = 0

        for id in times_idx:
            for i in range(len(df)):
                if int(df['times'][i]) == id and df['dates_ids'][i] >= 15 and df['dates_ids'][i] <= 28 and df['poles_ids'][i] == 3:
                    if df['Vehicle Type'][i] == 'small_vehicle':
                        y1_count += df['Count'][i]
                    elif df['Vehicle Type'][i]  == 'bus':
                        y2_count += df['Count'][i]
                    else:
                        y3_count += df['Count'][i]
            y1[times_idx.index(id)] = y1_count
            y2[times_idx.index(id)] = y2_count
            y3[times_idx.index(id)] = y3_count
            y1_count = 0
            y2_count = 0
            y3_count = 0

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y1,
            name='Small Vehicles',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y1)//len(y1) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of Small Vehicles across pole 3",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g2.plotly_chart(fig, use_container_width=True) 

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y2,
            name='Buses',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y2)//len(y2) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of Buses across pole 3",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g1.plotly_chart(fig, use_container_width=True) 

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y3,
            name='Large Vehicles',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y3)//len(y3) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of Large Vehicles across pole 3",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g2.plotly_chart(fig, use_container_width=True) 

        y1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        times_idx = list(range(0,24))

        y1_count = 0

        for id in times_idx:
            for i in range(len(df)):
                if int(df['times'][i]) == id and df['dates_ids'][i] >= 15 and df['dates_ids'][i] <= 28:
                    y1_count += df['Count'][i]
            y1[times_idx.index(id)] = y1_count
            y1_count = 0


        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y1,
            name='All Vehicles',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y1)//len(y1) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of All Vehicles",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        st.plotly_chart(fig, use_container_width=True)
        with st.form("my_form"):
            st.write("")
            Name = st.text_input('Name')
            Email = st.text_input('Email')
            submitted = st.form_submit_button("Send Alerts!")
            if submitted:
                send_email(Name,Email,small_vehicles_data, dates, 'Small Vehicles')
                send_email(Name,Email,buses_data, dates, 'Buses')
                send_email(Name,Email,large_vehicles_data, dates, 'Large Vehicles')


    elif '10/22/2022 to 11/04/2022' == report_range:
        g1, g2, g3 = st.columns((1,1,1))

        # Graph 1 - SV
        df = pd.read_csv('data/final_comprehensive_data.csv')
        y1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        dates_idx = list(range(29,43))

        y1_count = 0
        y2_count = 0
        y3_count = 0

        for id in dates_idx:
            for i in range(len(df)):
                if df['dates_ids'][i] == id:
                    if df['Vehicle Type'][i] == 'small_vehicle':
                        y1_count += df['Count'][i]
                    elif df['Vehicle Type'][i] == 'bus':
                        y2_count += df['Count'][i]
                    else:
                        y3_count += df['Count'][i]
            y1[dates_idx.index(id)] = y1_count
            y2[dates_idx.index(id)] = y2_count
            y3[dates_idx.index(id)] = y3_count
            y1_count = 0
            y2_count = 0
            y3_count = 0
        
        dates = ['10/22','10/23','10/24','10/25','10/26','10/27','10/28','10/29','10/30','10/31','11/01','11/02','11/03','11/04']

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=y1,
            name='Small Vehicles',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=dates, y=[sum(y1)//len(y1) for i in range(1,15)], mode='lines', line=dict(color="black"), name='Target')
        fig.update_layout(title_text="Flow of Small Vehicles",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g1.plotly_chart(fig, use_container_width=True) 
        small_vehicles_data = y1
        # Graph 2 - Buses
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=y2,
            name='Buses',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=dates, y=[sum(y2)//len(y2) for i in range(1,15)], mode='lines', line=dict(color="black"), name='Target')
        fig.update_layout(title_text="Flow of Buses",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))       
        g2.plotly_chart(fig, use_container_width=True) 

        buses_data = y2
        # Graph 3 - LV
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=y3,
            name='Large Vehicles',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=dates, y=[sum(y3)//len(y3) for i in range(1,15)], mode='lines', line=dict(color="black"), name='Target')
        fig.update_layout(title_text="Flow of Large Vehicles",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))       
        g3.plotly_chart(fig, use_container_width=True) 

        large_vehicles_data = y3
        # Graph 4 - Pole 1: SV

        y1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        dates_idx = list(range(29,43))

        y1_count = 0
        y2_count = 0
        y3_count = 0

        for id in dates_idx:
            for i in range(len(df)):
                if df['dates_ids'][i] == id and df['poles_ids'][i] == 1:
                    if df['Vehicle Type'][i] == 'small_vehicle':
                        y1_count += df['Count'][i]
                    elif df['Vehicle Type'][i] == 'bus':
                        y2_count += df['Count'][i]
                    else:
                        y3_count += df['Count'][i]
            y1[dates_idx.index(id)] = y1_count
            y2[dates_idx.index(id)] = y2_count
            y3[dates_idx.index(id)] = y3_count
            y1_count = 0
            y2_count = 0
            y3_count = 0
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=y1,
            name='Small Vehicles',
            marker_color='lightseagreen'
        ))
        fig.add_scatter(x=dates, y=[sum(y1)//len(y1) for i in range(1,15)], mode='lines', line=dict(color="black"), name='Target')
        fig.update_layout(title_text="Flow of Small Vehicles across pole 1",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g1.plotly_chart(fig, use_container_width=True) 
        
        # Graph 2 - Pole 1: Buses
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=y2,
            name='Buses',
            marker_color='lightseagreen'
        ))
        fig.add_scatter(x=dates, y=[sum(y2)//len(y2) for i in range(1,15)], mode='lines', line=dict(color="black"), name='Target')
        fig.update_layout(title_text="Flow of Buses across pole 1",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))       
        g2.plotly_chart(fig, use_container_width=True) 

        # Graph 3 - Pole 1: LV
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=y3,
            name='Large Vehicles',
            marker_color='lightseagreen'
        ))
        fig.add_scatter(x=dates, y=[sum(y3)//len(y3) for i in range(1,15)], mode='lines', line=dict(color="black"), name='Target')
        fig.update_layout(title_text="Flow of Large Vehicles across pole 1",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))       
        g3.plotly_chart(fig, use_container_width=True) 


        # Graph 4 - Pole 2: SV

        y1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        dates_idx = list(range(29,43))

        y1_count = 0
        y2_count = 0
        y3_count = 0

        for id in dates_idx:
            for i in range(len(df)):
                if df['dates_ids'][i] == id and df['poles_ids'][i] == 2:
                    if df['Vehicle Type'][i] == 'small_vehicle':
                        y1_count += df['Count'][i]
                    elif df['Vehicle Type'][i] == 'bus':
                        y2_count += df['Count'][i]
                    else:
                        y3_count += df['Count'][i]
            y1[dates_idx.index(id)] = y1_count
            y2[dates_idx.index(id)] = y2_count
            y3[dates_idx.index(id)] = y3_count
            y1_count = 0
            y2_count = 0
            y3_count = 0
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=y1,
            name='Small Vehicles',
            marker_color='lightcoral'
        ))
        fig.add_scatter(x=dates, y=[sum(y1)//len(y1) for i in range(1,15)], mode='lines', line=dict(color="black"), name='Target')
        fig.update_layout(title_text="Flow of Small Vehicles across pole 2",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g1.plotly_chart(fig, use_container_width=True) 
        
        # Graph 2 - Pole 2: Buses
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=y2,
            name='Buses',
            marker_color='lightcoral'
        ))
        fig.add_scatter(x=dates, y=[sum(y2)//len(y2) for i in range(1,15)], mode='lines', line=dict(color="black"), name='Target')
        fig.update_layout(title_text="Flow of Buses across pole 2",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))       
        g2.plotly_chart(fig, use_container_width=True) 

        # Graph 3 - Pole 2: LV
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=y3,
            name='Large Vehicles',
            marker_color='lightcoral'
        ))
        fig.add_scatter(x=dates, y=[sum(y3)//len(y3) for i in range(1,15)], mode='lines', line=dict(color="black"), name='Target')
        fig.update_layout(title_text="Flow of Large Vehicles across pole 2",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))       
        g3.plotly_chart(fig, use_container_width=True) 

    # Graph 4 - Pole 3: SV

        y1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        dates_idx = list(range(29,43))

        y1_count = 0
        y2_count = 0
        y3_count = 0

        for id in dates_idx:
            for i in range(len(df)):
                if df['dates_ids'][i] == id and df['poles_ids'][i] == 3:
                    if df['Vehicle Type'][i] == 'small_vehicle':
                        y1_count += df['Count'][i]
                    elif df['Vehicle Type'][i] == 'bus':
                        y2_count += df['Count'][i]
                    else:
                        y3_count += df['Count'][i]
            y1[dates_idx.index(id)] = y1_count
            y2[dates_idx.index(id)] = y2_count
            y3[dates_idx.index(id)] = y3_count
            y1_count = 0
            y2_count = 0
            y3_count = 0
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=y1,
            name='Small Vehicles',
            marker_color='lightsalmon'
        ))
        fig.add_scatter(x=dates, y=[sum(y1)//len(y1) for i in range(1,15)], mode='lines', line=dict(color="black"), name='Target')
        fig.update_layout(title_text="Flow of Small Vehicles across pole 3",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g1.plotly_chart(fig, use_container_width=True) 
        
        # Graph 2 - Pole 3: Buses
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=y2,
            name='Buses',
            marker_color='lightsalmon'
        ))
        fig.add_scatter(x=dates, y=[sum(y2)//len(y2) for i in range(1,15)], mode='lines', line=dict(color="black"), name='Target')
        fig.update_layout(title_text="Flow of Buses across pole 3",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))       
        g2.plotly_chart(fig, use_container_width=True) 

        # Graph 3 - Pole 3: LV
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=y3,
            name='Large Vehicles',
            marker_color='lightsalmon'
        ))
        fig.add_scatter(x=dates, y=[sum(y3)//len(y3) for i in range(1,15)], mode='lines', line=dict(color="black"), name='Target')
        fig.update_layout(title_text="Flow of Large Vehicles across pole 3",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))       
        g3.plotly_chart(fig, use_container_width=True) 

        g1,g2 = st.columns((1,1))    

        y1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        times_idx = list(range(0,24))

        y1_count = 0
        y2_count = 0
        y3_count = 0

        for id in times_idx:
            for i in range(len(df)):
                if int(df['times'][i]) == id and df['dates_ids'][i] >= 29 and df['dates_ids'][i] <= 42:
                    if df['Vehicle Type'][i] == 'small_vehicle':
                        y1_count += df['Count'][i]
                    elif df['Vehicle Type'][i]  == 'bus':
                        y2_count += df['Count'][i]
                    else:
                        y3_count += df['Count'][i]
            y1[times_idx.index(id)] = y1_count
            y2[times_idx.index(id)] = y2_count
            y3[times_idx.index(id)] = y3_count
            y1_count = 0
            y2_count = 0
            y3_count = 0
        
        times = ['0:00 AM','1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM']

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y1,
            name='Small Vehicles',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y1)//len(y1) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of Small Vehicles",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g1.plotly_chart(fig, use_container_width=True) 

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y2,
            name='Buses',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y2)//len(y2) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of Buses",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g2.plotly_chart(fig, use_container_width=True) 

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y3,
            name='Large Vehicles',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y3)//len(y3) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of Large Vehicles",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g1.plotly_chart(fig, use_container_width=True) 

        y1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        times_idx = list(range(0,24))

        y1_count = 0
        y2_count = 0
        y3_count = 0

        for id in times_idx:
            for i in range(len(df)):
                if int(df['times'][i]) == id and df['dates_ids'][i] >= 29 and df['dates_ids'][i] <= 42 and df['poles_ids'][i] == 1:
                    if df['Vehicle Type'][i] == 'small_vehicle':
                        y1_count += df['Count'][i]
                    elif df['Vehicle Type'][i]  == 'bus':
                        y2_count += df['Count'][i]
                    else:
                        y3_count += df['Count'][i]
            y1[times_idx.index(id)] = y1_count
            y2[times_idx.index(id)] = y2_count
            y3[times_idx.index(id)] = y3_count
            y1_count = 0
            y2_count = 0
            y3_count = 0
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y1,
            name='Small Vehicles',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y1)//len(y1) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of Small Vehicles across pole 1",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g2.plotly_chart(fig, use_container_width=True) 

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y2,
            name='Buses',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y2)//len(y2) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of Buses across pole 1",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g1.plotly_chart(fig, use_container_width=True) 

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y3,
            name='Large Vehicles',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y3)//len(y3) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of Large Vehicles across pole 1",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g2.plotly_chart(fig, use_container_width=True) 

        y1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        times_idx = list(range(0,24))

        y1_count = 0
        y2_count = 0
        y3_count = 0

        for id in times_idx:
            for i in range(len(df)):
                if int(df['times'][i]) == id and df['dates_ids'][i] >= 29 and df['dates_ids'][i] <= 42 and df['poles_ids'][i] == 2:
                    if df['Vehicle Type'][i] == 'small_vehicle':
                        y1_count += df['Count'][i]
                    elif df['Vehicle Type'][i]  == 'bus':
                        y2_count += df['Count'][i]
                    else:
                        y3_count += df['Count'][i]
            y1[times_idx.index(id)] = y1_count
            y2[times_idx.index(id)] = y2_count
            y3[times_idx.index(id)] = y3_count
            y1_count = 0
            y2_count = 0
            y3_count = 0
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y1,
            name='Small Vehicles',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y1)//len(y1) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of Small Vehicles across pole 2",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g1.plotly_chart(fig, use_container_width=True) 

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y2,
            name='Buses',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y2)//len(y2) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of Buses across pole 2",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g2.plotly_chart(fig, use_container_width=True) 

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y3,
            name='Large Vehicles',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y3)//len(y3) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of Large Vehicles across pole 2",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g1.plotly_chart(fig, use_container_width=True) 

        y1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        times_idx = list(range(0,24))

        y1_count = 0
        y2_count = 0
        y3_count = 0

        for id in times_idx:
            for i in range(len(df)):
                if int(df['times'][i]) == id and df['dates_ids'][i] >= 29 and df['dates_ids'][i] <= 42 and df['poles_ids'][i] == 3:
                    if df['Vehicle Type'][i] == 'small_vehicle':
                        y1_count += df['Count'][i]
                    elif df['Vehicle Type'][i]  == 'bus':
                        y2_count += df['Count'][i]
                    else:
                        y3_count += df['Count'][i]
            y1[times_idx.index(id)] = y1_count
            y2[times_idx.index(id)] = y2_count
            y3[times_idx.index(id)] = y3_count
            y1_count = 0
            y2_count = 0
            y3_count = 0

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y1,
            name='Small Vehicles',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y1)//len(y1) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of Small Vehicles across pole 3",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g2.plotly_chart(fig, use_container_width=True) 

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y2,
            name='Buses',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y2)//len(y2) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of Buses across pole 3",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g1.plotly_chart(fig, use_container_width=True) 

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y3,
            name='Large Vehicles',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y3)//len(y3) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of Large Vehicles across pole 3",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g2.plotly_chart(fig, use_container_width=True) 

        y1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        times_idx = list(range(0,24))

        y1_count = 0

        for id in times_idx:
            for i in range(len(df)):
                if int(df['times'][i]) == id and df['dates_ids'][i] >= 29 and df['dates_ids'][i] <= 42:
                    y1_count += df['Count'][i]
            y1[times_idx.index(id)] = y1_count
            y1_count = 0


        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y1,
            name='All Vehicles',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y1)//len(y1) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of All Vehicles",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        st.plotly_chart(fig, use_container_width=True)
        with st.form("my_form"):
            st.write("")
            Name = st.text_input('Name')
            Email = st.text_input('Email')
            submitted = st.form_submit_button("Send Alerts!")
            if submitted:
                send_email(Name,Email,small_vehicles_data, dates, 'Small Vehicles')
                send_email(Name,Email,buses_data, dates, 'Buses')
                send_email(Name,Email,large_vehicles_data, dates, 'Large Vehicles')

    else:
        g1, g2, g3 = st.columns((1,1,1))

        # Graph 1 - SV
        df = pd.read_csv('data/final_comprehensive_data.csv')
        y1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        dates_idx = list(range(1,43))

        y1_count = 0
        y2_count = 0
        y3_count = 0

        for id in dates_idx:
            for i in range(len(df)):
                if df['dates_ids'][i] == id:
                    if df['Vehicle Type'][i] == 'small_vehicle':
                        y1_count += df['Count'][i]
                    elif df['Vehicle Type'][i] == 'bus':
                        y2_count += df['Count'][i]
                    else:
                        y3_count += df['Count'][i]
            y1[dates_idx.index(id)] = y1_count
            y2[dates_idx.index(id)] = y2_count
            y3[dates_idx.index(id)] = y3_count
            y1_count = 0
            y2_count = 0
            y3_count = 0
        
        dates = ['09/24','09/25','09/26','09/27','09/28','09/29','09/30','10/01','10/02','10/03','10/04','10/05','10/06','10/07','10/08','10/09','10/10','10/11','10/12','10/13','10/14','10/15','10/16','10/17','10/18','10/19','10/20','10/21','10/22','10/23','10/24','10/25','10/26','10/27','10/28','10/29','10/30','10/31','11/01','11/02','11/03','11/04']

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=y1,
            name='Small Vehicles',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=dates, y=[sum(y1)//len(y1) for i in range(1,43)], mode='lines', line=dict(color="black"), name='Target')
        fig.update_layout(title_text="Flow of Small Vehicles",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g1.plotly_chart(fig, use_container_width=True) 
        
        small_vehicles_data = y1

        # Graph 2 - Buses
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=y2,
            name='Buses',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=dates, y=[sum(y2)//len(y2) for i in range(1,43)], mode='lines', line=dict(color="black"), name='Target')
        fig.update_layout(title_text="Flow of Buses",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))       
        g2.plotly_chart(fig, use_container_width=True) 

        buses_data = y2
        # Graph 3 - LV
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=y3,
            name='Large Vehicles',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=dates, y=[sum(y3)//len(y3) for i in range(1,43)], mode='lines', line=dict(color="black"), name='Target')
        fig.update_layout(title_text="Flow of Large Vehicles",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))       
        g3.plotly_chart(fig, use_container_width=True) 

        large_vehicles_data = y3
        # Graph 4 - Pole 1: SV

        y1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        dates_idx = list(range(1,43))

        y1_count = 0
        y2_count = 0
        y3_count = 0

        for id in dates_idx:
            for i in range(len(df)):
                if df['dates_ids'][i] == id and df['poles_ids'][i] == 1:
                    if df['Vehicle Type'][i] == 'small_vehicle':
                        y1_count += df['Count'][i]
                    elif df['Vehicle Type'][i] == 'bus':
                        y2_count += df['Count'][i]
                    else:
                        y3_count += df['Count'][i]
            y1[dates_idx.index(id)] = y1_count
            y2[dates_idx.index(id)] = y2_count
            y3[dates_idx.index(id)] = y3_count
            y1_count = 0
            y2_count = 0
            y3_count = 0
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=y1,
            name='Small Vehicles',
            marker_color='lightseagreen'
        ))
        fig.add_scatter(x=dates, y=[sum(y1)//len(y1) for i in range(1,43)], mode='lines', line=dict(color="black"), name='Target')
        fig.update_layout(title_text="Flow of Small Vehicles across pole 1",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g1.plotly_chart(fig, use_container_width=True) 
        
        # Graph 2 - Pole 1: Buses
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=y2,
            name='Buses',
            marker_color='lightseagreen'
        ))
        fig.add_scatter(x=dates, y=[sum(y2)//len(y2) for i in range(1,43)], mode='lines', line=dict(color="black"), name='Target')
        fig.update_layout(title_text="Flow of Buses across pole 1",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))       
        g2.plotly_chart(fig, use_container_width=True) 

        # Graph 3 - Pole 1: LV
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=y3,
            name='Large Vehicles',
            marker_color='lightseagreen'
        ))
        fig.add_scatter(x=dates, y=[sum(y3)//len(y3) for i in range(1,43)], mode='lines', line=dict(color="black"), name='Target')
        fig.update_layout(title_text="Flow of Large Vehicles across pole 1",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))       
        g3.plotly_chart(fig, use_container_width=True) 


        # Graph 4 - Pole 2: SV

        y1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        dates_idx = list(range(1,43))

        y1_count = 0
        y2_count = 0
        y3_count = 0

        for id in dates_idx:
            for i in range(len(df)):
                if df['dates_ids'][i] == id and df['poles_ids'][i] == 2:
                    if df['Vehicle Type'][i] == 'small_vehicle':
                        y1_count += df['Count'][i]
                    elif df['Vehicle Type'][i] == 'bus':
                        y2_count += df['Count'][i]
                    else:
                        y3_count += df['Count'][i]
            y1[dates_idx.index(id)] = y1_count
            y2[dates_idx.index(id)] = y2_count
            y3[dates_idx.index(id)] = y3_count
            y1_count = 0
            y2_count = 0
            y3_count = 0
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=y1,
            name='Small Vehicles',
            marker_color='lightcoral'
        ))
        fig.add_scatter(x=dates, y=[sum(y1)//len(y1) for i in range(1,43)], mode='lines', line=dict(color="black"), name='Target')
        fig.update_layout(title_text="Flow of Small Vehicles across pole 2",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g1.plotly_chart(fig, use_container_width=True) 
        
        # Graph 2 - Pole 2: Buses
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=y2,
            name='Buses',
            marker_color='lightcoral'
        ))
        fig.add_scatter(x=dates, y=[sum(y2)//len(y2) for i in range(1,43)], mode='lines', line=dict(color="black"), name='Target')
        fig.update_layout(title_text="Flow of Buses across pole 2",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))       
        g2.plotly_chart(fig, use_container_width=True) 

        # Graph 3 - Pole 2: LV
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=y3,
            name='Large Vehicles',
            marker_color='lightcoral'
        ))
        fig.add_scatter(x=dates, y=[sum(y3)//len(y3) for i in range(1,43)], mode='lines', line=dict(color="black"), name='Target')
        fig.update_layout(title_text="Flow of Large Vehicles across pole 2",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))       
        g3.plotly_chart(fig, use_container_width=True) 

    # Graph 4 - Pole 3: SV

        y1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        dates_idx = list(range(1,43))

        y1_count = 0
        y2_count = 0
        y3_count = 0

        for id in dates_idx:
            for i in range(len(df)):
                if df['dates_ids'][i] == id and df['poles_ids'][i] == 3:
                    if df['Vehicle Type'][i] == 'small_vehicle':
                        y1_count += df['Count'][i]
                    elif df['Vehicle Type'][i] == 'bus':
                        y2_count += df['Count'][i]
                    else:
                        y3_count += df['Count'][i]
            y1[dates_idx.index(id)] = y1_count
            y2[dates_idx.index(id)] = y2_count
            y3[dates_idx.index(id)] = y3_count
            y1_count = 0
            y2_count = 0
            y3_count = 0
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=y1,
            name='Small Vehicles',
            marker_color='lightsalmon'
        ))
        fig.add_scatter(x=dates, y=[sum(y1)//len(y1) for i in range(1,43)], mode='lines', line=dict(color="black"), name='Target')
        fig.update_layout(title_text="Flow of Small Vehicles across pole 3",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g1.plotly_chart(fig, use_container_width=True) 
        
        # Graph 2 - Pole 3: Buses
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=y2,
            name='Buses',
            marker_color='lightsalmon'
        ))
        fig.add_scatter(x=dates, y=[sum(y2)//len(y2) for i in range(1,43)], mode='lines', line=dict(color="black"), name='Target')
        fig.update_layout(title_text="Flow of Buses across pole 3",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))       
        g2.plotly_chart(fig, use_container_width=True) 

        # Graph 3 - Pole 3: LV
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates,
            y=y3,
            name='Large Vehicles',
            marker_color='lightsalmon'
        ))
        fig.add_scatter(x=dates, y=[sum(y3)//len(y3) for i in range(1,43)], mode='lines', line=dict(color="black"), name='Target')
        fig.update_layout(title_text="Flow of Large Vehicles across pole 3",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))       
        g3.plotly_chart(fig, use_container_width=True) 

        g1,g2 = st.columns((1,1))    

        y1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        times_idx = list(range(0,24))

        y1_count = 0
        y2_count = 0
        y3_count = 0

        for id in times_idx:
            for i in range(len(df)):
                if int(df['times'][i]) == id:
                    if df['Vehicle Type'][i] == 'small_vehicle':
                        y1_count += df['Count'][i]
                    elif df['Vehicle Type'][i]  == 'bus':
                        y2_count += df['Count'][i]
                    else:
                        y3_count += df['Count'][i]
            y1[times_idx.index(id)] = y1_count
            y2[times_idx.index(id)] = y2_count
            y3[times_idx.index(id)] = y3_count
            y1_count = 0
            y2_count = 0
            y3_count = 0
        
        times = ['0:00 AM','1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM']

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y1,
            name='Small Vehicles',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y1)//len(y1) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of Small Vehicles",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g1.plotly_chart(fig, use_container_width=True) 

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y2,
            name='Buses',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y2)//len(y2) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of Buses",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g2.plotly_chart(fig, use_container_width=True) 

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y3,
            name='Large Vehicles',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y3)//len(y3) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of Large Vehicles",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g1.plotly_chart(fig, use_container_width=True) 

        y1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        times_idx = list(range(0,24))

        y1_count = 0
        y2_count = 0
        y3_count = 0

        for id in times_idx:
            for i in range(len(df)):
                if int(df['times'][i]) == id and df['poles_ids'][i] == 1:
                    if df['Vehicle Type'][i] == 'small_vehicle':
                        y1_count += df['Count'][i]
                    elif df['Vehicle Type'][i]  == 'bus':
                        y2_count += df['Count'][i]
                    else:
                        y3_count += df['Count'][i]
            y1[times_idx.index(id)] = y1_count
            y2[times_idx.index(id)] = y2_count
            y3[times_idx.index(id)] = y3_count
            y1_count = 0
            y2_count = 0
            y3_count = 0
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y1,
            name='Small Vehicles',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y1)//len(y1) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of Small Vehicles across pole 1",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g2.plotly_chart(fig, use_container_width=True) 

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y2,
            name='Buses',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y2)//len(y2) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of Buses across pole 1",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g1.plotly_chart(fig, use_container_width=True) 

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y3,
            name='Large Vehicles',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y3)//len(y3) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of Large Vehicles across pole 1",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g2.plotly_chart(fig, use_container_width=True) 

        y1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        times_idx = list(range(0,24))

        y1_count = 0
        y2_count = 0
        y3_count = 0

        for id in times_idx:
            for i in range(len(df)):
                if int(df['times'][i]) == id and df['poles_ids'][i] == 2:
                    if df['Vehicle Type'][i] == 'small_vehicle':
                        y1_count += df['Count'][i]
                    elif df['Vehicle Type'][i]  == 'bus':
                        y2_count += df['Count'][i]
                    else:
                        y3_count += df['Count'][i]
            y1[times_idx.index(id)] = y1_count
            y2[times_idx.index(id)] = y2_count
            y3[times_idx.index(id)] = y3_count
            y1_count = 0
            y2_count = 0
            y3_count = 0
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y1,
            name='Small Vehicles',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y1)//len(y1) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of Small Vehicles across pole 2",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g1.plotly_chart(fig, use_container_width=True) 

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y2,
            name='Buses',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y2)//len(y2) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of Buses across pole 2",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g2.plotly_chart(fig, use_container_width=True) 

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y3,
            name='Large Vehicles',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y3)//len(y3) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of Large Vehicles across pole 2",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g1.plotly_chart(fig, use_container_width=True) 

        y1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        y3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        times_idx = list(range(0,24))

        y1_count = 0
        y2_count = 0
        y3_count = 0

        for id in times_idx:
            for i in range(len(df)):
                if int(df['times'][i]) == id and df['poles_ids'][i] == 3:
                    if df['Vehicle Type'][i] == 'small_vehicle':
                        y1_count += df['Count'][i]
                    elif df['Vehicle Type'][i]  == 'bus':
                        y2_count += df['Count'][i]
                    else:
                        y3_count += df['Count'][i]
            y1[times_idx.index(id)] = y1_count
            y2[times_idx.index(id)] = y2_count
            y3[times_idx.index(id)] = y3_count
            y1_count = 0
            y2_count = 0
            y3_count = 0

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y1,
            name='Small Vehicles',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y1)//len(y1) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of Small Vehicles across pole 3",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g2.plotly_chart(fig, use_container_width=True) 

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y2,
            name='Buses',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y2)//len(y2) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of Buses across pole 3",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g1.plotly_chart(fig, use_container_width=True) 

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y3,
            name='Large Vehicles',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y3)//len(y3) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of Large Vehicles across pole 3",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        g2.plotly_chart(fig, use_container_width=True) 

        y1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        times_idx = list(range(0,24))

        y1_count = 0

        for id in times_idx:
            for i in range(len(df)):
                if int(df['times'][i]) == id:
                    y1_count += df['Count'][i]
            y1[times_idx.index(id)] = y1_count
            y1_count = 0


        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=times,
            y=y1,
            name='All Vehicles',
            marker_color='darkslateblue'
        ))
        fig.add_scatter(x=times, y=[sum(y1)//len(y1) for i in range(1,25)], mode='lines', line=dict(color="black"), name='Target')
        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(title_text="Flow of All Vehicles",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title='Count', xaxis_title='Date', legend=dict(orientation="h",yanchor="bottom",y=0.9,xanchor="right",x=0.99))
        st.plotly_chart(fig, use_container_width=True)
        with st.form("my_form"):
            st.write("")
            Name = st.text_input('Name')
            Email = st.text_input('Email')
            submitted = st.form_submit_button("Send Alerts!")
            if submitted:
                send_email(Name,Email,small_vehicles_data, dates, 'Small Vehicles')
                send_email(Name,Email,buses_data, dates, 'Buses')
                send_email(Name,Email,large_vehicles_data, dates, 'Large Vehicles')

with st.spinner('Report updated!'):
    time.sleep(1)     