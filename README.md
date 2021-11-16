@[TOC](基于课程标签分类的智能推荐专家系统（Python+PyQt5实现）)

# 写在前面
项目名称：基于课程标签分类的智能推荐专家系统v1.0

软件环境：Windows 10 64位

硬件环境：

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

![在这里插入图片描述](https://img-blog.csdnimg.cn/9793bb156c55489c913b3d8758bbb533.png?x-oss-process=image/watermark,type_ZHJvaWRzYW5zZmFsbGJhY2s,shadow_50,text_Q1NETiBAc2dzeDEx,size_20,color_FFFFFF,t_70,g_se,x_16)
添加规则：

![在这里插入图片描述](https://img-blog.csdnimg.cn/ec80da46bd564439a9f8f2e786f977cb.png)

![在这里插入图片描述](https://img-blog.csdnimg.cn/07c7a50cdc3349f1b5ec048a474b80ff.png?x-oss-process=image/watermark,type_ZHJvaWRzYW5zZmFsbGJhY2s,shadow_50,text_Q1NETiBAc2dzeDEx,size_19,color_FFFFFF,t_70,g_se,x_16)
开始推理：

![在这里插入图片描述](https://img-blog.csdnimg.cn/7894488757a846a7879a725ae0f556f7.png)

![在这里插入图片描述](https://img-blog.csdnimg.cn/67fe63ab1fab43c5aab43ebe295a8ac5.png)

![在这里插入图片描述](https://img-blog.csdnimg.cn/447d01656d84484eb76bfc3ecfc194bd.png?x-oss-process=image/watermark,type_ZHJvaWRzYW5zZmFsbGJhY2s,shadow_50,text_Q1NETiBAc2dzeDEx,size_20,color_FFFFFF,t_70,g_se,x_16)

