class MatchType():
  pass


class LocalMultiplayer(MatchType):
  pass


class LocalAI(MatchType):
  AI_DIFFICULTY_EASY = 1

  def __init__(self, difficulty):
    self.difficulty = difficulty


class LANMultiplayer(MatchType):
  def __init__(self, host):
    self.host = host
