class FinishButtonException(Exception):
    def __str__(self):
        return "終了ボタン押下"


class MyException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(args)
        for key in kwargs:
            setattr(self, key, kwargs[key])


class SkipException(MyException):
    def __str__(self):
        return "次の処理にスキップ"


class HasEvent(MyException):
    def __str__(self):
        return "イベントあり"


class CannotFindException(MyException):
    def __str__(self):
        return "敵が見つかりません"


class QuestNotFinish(MyException):
    def __str__(self):
        return "クエストが終了しません"


class BattleNotFinish(MyException):
    def __str__(self):
        return "バトルが終了しません"


class NextQuestNotStart(MyException):
    def __str__(self):
        return "次のクエストが開始しません"


class NotInBattle(MyException):
    def __str__(self):
        return "戦闘していません"


class NextAlreadyStarted(MyException):
    def __str__(self):
        return "既に次のクエストです"


class SceneError(MyException):
    pass


class TransitionError(MyException):
    pass
