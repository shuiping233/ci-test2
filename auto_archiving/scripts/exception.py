class ErrorMessage():
    '''自定义异常信息'''

    unknown_action_name = "未知的action类型：｛action_name｝，无法找到与之对应的issue仓库类型"
    


class ArchiveBaseError(Exception):
    "归档错误的基类"

class ArchiveVersionError(ArchiveBaseError):
    '''issue评论中找不到归档关键字，缺少归档版本号等'''
    pass


class IntroducedVersionError(ArchiveBaseError):
    '''issue描述中缺少声明引入版本号的格式文本，缺少引入版本号等'''
    pass


class ArchiveLabelError(ArchiveBaseError):
    '''缺少关键的归档标签等'''
    pass

class IssueTypeError(ArchiveBaseError):
    '''issue标题中缺少issue类型声明关键字等'''



class InBlackList(ArchiveBaseError):
    '''匹配到无法继续执行归档任务的黑名单内容'''
    pass


