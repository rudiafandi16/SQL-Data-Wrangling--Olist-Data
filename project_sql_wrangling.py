#!/usr/bin/env python
# coding: utf-8

# <h1 style="color:black; font-size:36px">Import Dataset</h1>

# In[2]:


# Import library yang akan digunakan
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[3]:


#Fungsi untuk menampilkan data dalam tabel dari database
def get_result(query):
    conn = sqlite3.connect("olist.db")
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data

def create_df(data, columns):
    return pd.DataFrame(data=data, columns=columns).drop(["index"], axis=1)


# In[5]:


#Memanggil tabel yang dibutuhkan
olist_order_customer_dataset = create_df(get_result("SELECT * FROM olist_order_customer_dataset"), ["index", "customer_id", "customers_uniq_id", "customers_zip_code_prefix","customers_city", "customers_state"])
olist_order_dataset = create_df(get_result("SELECT * FROM olist_order_dataset"), ["index", "order_id", "customer_id", "order_status","order_purchase_timestamp", "order_approved_at","order_delivered_carries_date", "order_delivered_customer_date", "order_estimated_delivery_date"])
olist_order_payments_dataset = create_df(get_result("SELECT * FROM olist_order_payments_dataset"), ["index", "order_id", "payment_sequential", "payment_type", "payment_installments", "payment_value"])
olist_order_items_dataset = create_df(get_result("SELECT * FROM olist_order_items_dataset"), ["index", "order_id", "order_item_id", "product_id", "seller_id", "shipping_limit_date", "price", "freight_value"])
olist_products_dataset =create_df(get_result("SELECT * FROM olist_products_dataset"), ["index", "product_id", "product_category_name", "product_name_lenght", "product_description_lenght", "product_photos_qty", "product_weight_g", "product_length_cm", "product_height_cm", "product_width_cm"])


# <h1 style="color:black; font-size:32px">Table Customers</h1>

# In[34]:


olist_order_customer_dataset


# <h1 style="color:black; font-size:32px">Table Orders</h1>

# In[5]:


olist_order_dataset


# #<h1 style="color:black; font-size:32px">Table Payments</h1>

# In[6]:


olist_order_payments_dataset


# <h1 style="color:black; font-size:32px">Table Items</h1>

# In[7]:


olist_order_items_dataset


# <h1 style="color:black; font-size:32px">Table Products</h1>

# In[8]:


olist_products_dataset


# <h1 style="color:black; font-size:24px">Eksploratory Data</h1>
# 

# <h1 style="color:black; font-size:18px">Objective <br>
#     1. Mengetahui produk apa yang paling banyak dipesan oleh customer <br>
#     2. Mengetahui total value dari tiap-tiap produk <br>
#     3. Mengetahui wilayah dengan penjualan tertinggi </h1>

# <h1 style="color:black; font-size:18px">Data Preparation</h1>
# 

# <h1 style="color:black; font-size:16px">Mengecek data yang kosong pada tabel items </h1>

# In[9]:


# Inisialisasi nama menjadi lebih pendek
olist_order_items_dataset.isna().sum()


# <h1 style="color:black; font-size:16px">Mengecek data yang duplikat pada tabel items </h1>

# In[10]:


olist_order_items_dataset[olist_order_items_dataset.duplicated(keep=False)]


# <h1 style="color:black; font-size:16px">Mengecek data yang kosong pada tabel produk </h1>

# In[30]:


olist_products_dataset.isna().sum()


# Handle data yang kosong

# In[29]:


# mengisi nilai rata-rata
mean_values = olist_products_dataset[['product_name_lenght','product_description_lenght', 'product_photos_qty']].mean()
olist_products_dataset[['product_name_lenght','product_description_lenght', 'product_photos_qty']] = olist_products_dataset[['product_name_lenght','product_description_lenght', 'product_photos_qty']].fillna(mean_values)
olist_products_dataset['product_category_name'].fillna('unknown', inplace=False)
# mengisi nilai kosong pada kolom product_weight_g dengan median
median_value = olist_products_dataset['product_weight_g'].median()
olist_products_dataset['product_weight_g'].fillna(median_value, inplace=False)

# mengisi nilai kosong pada kolom product_length_cm dengan median
median_value = olist_products_dataset['product_length_cm'].median()
olist_products_dataset['product_length_cm'].fillna(median_value, inplace=False)

# mengisi nilai kosong pada kolom product_height_cm dengan median
median_value = olist_products_dataset['product_height_cm'].median()
olist_products_dataset['product_height_cm'].fillna(median_value, inplace=False)

# mengisi nilai kosong pada kolom product_width_cm dengan median
median_value = olist_products_dataset['product_width_cm'].median()
olist_products_dataset['product_width_cm'].fillna(median_value, inplace=False)

# melakukan drop pada baris dengan nilai kosong
olist_products_dataset.dropna(inplace=False)


# <h1 style="color:black; font-size:16px">Mengecek data yang duplikat pada tabel produk </h1>

# In[12]:


olist_products_dataset[olist_products_dataset.duplicated(keep=False)]


# <h1 style="color:black; font-size:18px">1. Objektif untuk mengetahui 10 produk yang paling banyak diorder</h1>

# <h1 style="color:black; font-size:16px"> Menggabungkan tabel item dengan tabel produk </h1>

# In[13]:


TABLE1 = pd.merge(olist_order_items_dataset, olist_products_dataset, on= "product_id", how= "left")


# In[14]:


#Memampilkan 5 data teratas
TABLE1.head()


# In[15]:


TABLE2 = TABLE1.rename({"product_category_name":"product_category" , "order_id":"order_counts"}, axis=1)
TABLE2 = TABLE2[["product_category","order_counts"]].groupby("product_category").count()
TABLE2 = TABLE2.sort_values("order_counts", ascending= False).reset_index()

TABLE2


# In[49]:


f, ax = plt.subplots(figsize=(10, 15))

# Mengambil 10 data teratas dari DataFrame TABLE6
top_10_TABLE2 = TABLE2.head(10)

sns.barplot(y="product_category", x="order_counts", data=top_10_TABLE2, color="limegreen")
sns.set_style("whitegrid")

ax.set(ylabel ="product_category", xlabel="order", title="TOP 10 Data order dari masing masing Product Category")

for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)


# <h1 style="color:black; font-size:18px">2. Objektif untuk mengetahui 10 data teratas total value dari masing-masing produk</h1>

# <h1 style="color:black; font-size:16px"> Menggabungkan tabel</h1>

# In[17]:


TABLE3 = pd.merge(TABLE1, olist_order_payments_dataset, on="order_id", how="left")
TABLE3


# In[18]:


TABLE4 = TABLE3.rename({"product_category_name":"product_category", "payment_value":"value"}, axis=1)
TABLE4 = TABLE4[["product_category", "value"]].groupby("product_category").count()
TABLE4 = TABLE4.sort_values("value", ascending=False).reset_index()

TABLE4


# In[48]:


f, ax = plt.subplots(figsize=(10, 15))

# Mengambil 10 data teratas dari DataFrame TABLE6
top_10_TABLE4 = TABLE4.head(10)

sns.barplot(y="product_category", x="value", data=top_10_TABLE4, color="b")
sns.set_style("whitegrid")

ax.set(ylabel ="product_category", xlabel="value", title="TOP 10 Data value untuk tiap tiap produk kategori")

for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)


# <h1 style="color:black; font-size:18px">3. Objektif untuk mengetahui 10 daerah dengan penjualan tertinggi</h1>

# <h1 style="color:black; font-size:16px"> Menggabungkan tabel</h1>

# In[33]:


TABLE5 = pd.merge(olist_order_dataset, olist_order_customer_dataset, on= "customer_id", how="left")
TABLE5


# In[44]:


TABLE6 = TABLE5.rename({"customers_state":"daerah","order_id":"order_counts"}, axis=1)
TABLE6 = TABLE6[["daerah", "order_counts"]].groupby("daerah").count()
TABLE6 = TABLE6.sort_values("order_counts", ascending=False).reset_index()

TABLE6


# In[55]:


f, ax = plt.subplots(figsize=(10, 15))

# Mengambil 10 data teratas dari DataFrame TABLE6
top_10_TABLE6 = TABLE6.head(10)

sns.barplot(y="order_counts", x="daerah", data=top_10_TABLE6, color="orange")
sns.set_style("whitegrid")

ax.set(ylabel ="order_counts", xlabel="daerah", title="TOP 10 Data daerah yang mempunyai penjualan tinggi")

for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)


# In[ ]:




