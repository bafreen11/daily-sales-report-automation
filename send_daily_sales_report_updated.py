#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
print(os.getcwd())


# In[2]:


import pandas as pd
from email.message import EmailMessage
from datetime import datetime
import openpyxl
from openpyxl.chart import BarChart, Reference
import os

# Load CSV
df = pd.read_csv('D:\\Downloads\\Supermart_Grocery_Sales.csv')

# See column names
df.columns.tolist()


# In[3]:


# Clean column names: lowercase and strip spaces
df.columns = df.columns.str.lower().str.replace(' ', '_')
df.columns.tolist()  # Re-check column names now


# In[11]:


from datetime import datetime

# 2. Fix order_date column
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
df = df[df['order_date'].notnull()]

# 3. Add a fake row with today's date
fake_row = pd.DataFrame([{
    'order_id': 'TEST999',
    'customer_name': 'Test User',
    'category': 'Beverages',
    'sub_category': 'Tea',
    'city': 'Test City',
    'order_date': pd.to_datetime(datetime.now()),
    'region': 'South',
    'sales': 1000,
    'discount': 0.1,
    'profit': 250,
    'state': 'Test State'
}])

df = pd.concat([df, fake_row], ignore_index=True)


# In[12]:


# 4. Filter today's data
today = datetime.now().date()
df_today = df[df['order_date'].dt.date == today]


# In[13]:


df_today.shape


# In[14]:


summary_df = df_today.groupby('category')[['sales', 'profit']].sum().reset_index()
report_path = f'D:\\Downloads\\today_category_sales_{today}.xlsx'
summary_df.to_excel(report_path, index=False)

print("✅ Report saved:", report_path)
print(summary_df)


# In[7]:


import os
os.path.exists('D:\\Downloads')


# In[15]:


import smtplib
from email.message import EmailMessage
import os


# In[16]:


# ---------- 2. Send Email ----------
sender_email = 'bafreen11@gmail.com'
receiver_email = 'irfan2014.mohammed@gmai.com'  # Change to actual email
app_password = 'gdbwohybhxnjfhey'  # Replace with Gmail App Password
excel_path = 'D:\\Downloads\\today_category_sales.xlsx'  # ✅ use actual file path


# Create email message
msg = EmailMessage()
msg['Subject'] = f'Daily Category Sales Report - {today.strftime("%Y-%m-%d")}'
msg['From'] = sender_email
msg['To'] = receiver_email

# Email content
msg.set_content(f"""Hello Manager,

Please find attached the daily **Category-wise Sales Report** for {today.strftime("%Y-%m-%d")}.

Total categories: {len(summary_df)}
Total sales: ₹{summary_df['sales'].sum():,.2f}
Total profit: ₹{summary_df['profit'].sum():,.2f}

Regards,
Sales Automation Bot
""")

# Attach Excel report
# Define the report file path
report_path = f'D:\\Downloads\\today_category_sales_{datetime.now().date()}.xlsx'

with open(report_path, 'rb') as f:
    msg.add_attachment(f.read(), maintype='application', subtype='octet-stream',
                       filename=report_path.split('\\')[-1])

# Send via Gmail SMTP
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(sender_email, app_password)
    smtp.send_message(msg)

print("📧 Email sent successfully.")


# In[ ]:





# In[ ]:




