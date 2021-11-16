# 写在前面
项目名称：基于课程标签分类的智能推荐专家系统v1.0

软件环境：Windows 10 64位 家庭中文版

硬件环境：![image](https://user-images.githubusercontent.com/93324578/141996420-a5be3b8f-0e5b-4180-aed7-d02ac1f12481.png)

开发工具：Pycharm21.2

项目描述：上周的人工智能实验课要求我们做一个基于Python的简单的专家系统并用PyQt5实现图形化界面。于是我结合之前爬取的bilibili和慕课网的网课信息做了一个基于课程标签分类的智能推荐专家系统

参考文章：[基于Python/PYQT5的动物识别专家系统（人工智能实验）](https://blog.csdn.net/xiaotang_sama/article/details/84955884)

# 系统逻辑

推理：
 1. **遍历事实列表**，根据一个或多个事实(**调用itertools库中的combinations方法进行组合**)在规则库中查找结论
 2. 如果找到，判断该结论是否已存在**结论列表**中或者**事实列表**中，如果为否，则将结论加入事实列表，并存入结论列表，跳转（4）
 3. 如果没找到或者该结论已存在，**继续遍历**事实列表，回到（2）
 4. **重新遍历**事实列表，回到（1）
 5. 事实列表遍历完毕，如果结论列表不为空，则取结论列表中**最新**的结论输出为结果


# 图形界面展示

开始界面：

![image](https://user-images.githubusercontent.com/93324578/141995199-5c1dcfe5-938d-4edd-b181-cc0cf0a9a809.png)
添加规则：

![image](https://user-images.githubusercontent.com/93324578/141995430-cf612036-51ac-40bc-978f-085b0ec32fab.png)

![image](https://user-images.githubusercontent.com/93324578/141995463-0095fbbc-4b99-4538-831c-c8e39fd69e80.png)
开始推理：

![image](https://user-images.githubusercontent.com/93324578/141995538-cb746a5a-b9fc-4f7a-bdf1-6608af226d3d.png)

![image](https://user-images.githubusercontent.com/93324578/141995582-b0fbb648-3c03-486f-9b3f-38f61f9e79de.png)

![image](https://user-images.githubusercontent.com/93324578/141995817-5990157d-1083-4892-b269-f76a266c24ee.png)

