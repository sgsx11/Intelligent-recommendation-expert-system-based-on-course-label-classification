报错解决：
	一、Python读取xls文件报错：raise XLRDError(FILE_FORMAT_DESCRIPTIONS[file_format]+‘； not supported‘) 
		先删除已安装的xlrd
		pip uninstall xlrd
		再安装低版本xlrd搞定
		pip install xlrd==1.2.0

