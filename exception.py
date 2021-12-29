class FinishButtonException(Exception):
    def __str__(self):
        return "終了ボタン押下"


class SkipException(Exception):
    def __str__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])
        return "次の処理にスキップ"


class HasEvent(Exception):
    def __str__(self):
        return "イベントあり"


class CannotFindException(Exception):
    def __str__(self):
        return "敵が見つかりません"


class QuestNotFinish(Exception):
    def __str__(self):
        return "クエストが終了しません"


class BattleNotFinish(Exception):
    def __str__(self):
        return "バトルが終了しません"
