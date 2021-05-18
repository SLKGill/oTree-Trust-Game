from otree.api import *

c = Currency

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'my_trust'
    players_per_group = 2
    num_rounds = 1
    endowment = c(10)
    multiplication_factor = 3  # comment out if we changed it in settings with sessions


class Subsession(BaseSubsession):
    pass


#  def creating_subsession(self):
#     for i in self.get_groups():
#        i.multiplication_factor = self.session.config['multiplication_factor']
#         #extracts multiplication_factor from settings configs


class Group(BaseGroup):
    sent_amount = models.CurrencyField(
        label="How much do you want to send to participant B?",
        min=c(0),
        max=Constants.endowment
    )
    sent_back_amount = models.CurrencyField(
        label="How much do you want to send back"
    )

    # multiplication_factor = models.IntegerField()

    def sent_back_amount_choices(self):
        return currency_range(cu(0), self.sent_amount * Constants.multiplication_factor, cu(1))


def set_payoffs(self):
    p1 = self.get_player_by_id(1)
    p2 = self.get_player_by_id(2)
    p1.payoff = Constants.endowment - self.sent_amount + self.sent_back_amount
    p2.payoff = self.sent_amount * Constants.multiplication_factor - self.sent_back_amount


# this function is seperate to the group class


class Player(BasePlayer):
    pass


# PAGES
class Send(Page):
    form_model = 'group'
    form_fields = ['sent_amount']

    @staticmethod
    def is_displayed(player):  # only display to P1. P2 skips
        return player.id_in_group == 1


class WaitForP1(WaitPage):
    pass


class Sendback(Page):
    form_model = 'group'
    form_fields = ['sent_back_amount']

    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 2

    @staticmethod  # using this @ lets us use player as parameter, works
    def vars_for_template(player):
        return dict(
            tripled_amount=player.group.sent_amount * Constants.multiplication_factor
        )


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'  # triggers the function in group
    # need to refer to function set_payoffs with quotations


class Results(Page):
    pass


page_sequence = [Send, WaitForP1, Sendback, ResultsWaitPage, Results]
