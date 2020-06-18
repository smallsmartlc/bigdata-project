#代码来自简书NEO_X  https://www.jianshu.com/p/06d157ba1a08

from pyspark.sql import SparkSession
spark=SparkSession.builder.appName('lin_reg').getOrCreate()

# 2-读取数据
from pyspark.ml.regression import LinearRegression
#将爬取的数据上传hdfs后,修改文件读取地址
df=spark.read.csv('hdfs://localhost:9000/input_spark/res2.csv',inferSchema=True,header=True)

# 3-探索分析数据
print('-------------- 探索分析数据 -----------------')
print((df.count(), len(df.columns)))                 # 查看数据规模
df.printSchema()                                     # 查看数据结构类型
df.describe().show(5,False)                          # 查看数据集的统计数据,包括平均值，标准差，数量统计等。
from pyspark.sql.functions import corr
df.select(corr('square','price')).show()             # 计算数据方差

# 4-数据转换,适应模型算法中的要求
from pyspark.ml.linalg import Vector
from pyspark.ml.feature import VectorAssembler       # 导入库VectorAssembler

print('-------------- 数据转换 ------------------')
#修改列名
vec_assmebler=VectorAssembler(inputCols=['square', 'floors', 'rooms', 'subway', 'area'],outputCol='features') # 转换，这里相对将多元一次方程中的各变量存放到一个向量中
features_df=vec_assmebler.transform(df)             

features_df.printSchema() # 查看变换后的结构。

model_df=features_df.select('features','price')     # 构建用于线性回归的数据模型

# 5-将数据划分为 训练数据和预测数据
train_df,test_df=model_df.randomSplit([0.7,0.3])     # 训练数据和预测数据的比例为 7比3

print((train_df.count(), len(train_df.columns)))

print((test_df.count(), len(test_df.columns)))

# 6-构建线性回归模型

from pyspark.ml.regression import LinearRegression         # 导入线性回顾库

print('-------------- 构建线性回归模型 ------------------')

lin_Reg=LinearRegression(labelCol='price')                 # labelCol,相对于featrues列，表示要进行预测的列

lr_model=lin_Reg.fit(train_df)                              # 训练数据 ，fit返回一个 fitted model，即LineRegressionModel对象

print('{}{}'.format('方程截距:',lr_model.intercept))         # intercept 线性方程的截距。

print('{}{}'.format('方程参数系数:',lr_model.coefficients))  # 回归方程中的，变量参数 ,这里分别对应var_1,var_2,var_3,var_4,var_5

training_predictions=lr_model.evaluate(train_df)            # 查看预测数据

print('{}{}'.format('误差差值平方:',training_predictions.meanSquaredError))            # 误差值差值平方   

print('{}{}'.format('判定系数：',training_predictions.r2 ))  # r2 判定系数,用来判定，构建的模型是否能够准确的预测,越大说明预测的准确率越高

# 7-使用预测数据,用已经到构建好的预测模型 lr_model
test_results=lr_model.evaluate(test_df)

print(test_results.r2)                              # 查看预测的拟合程度
print(test_results.meanSquaredError)                # 查看均方误差