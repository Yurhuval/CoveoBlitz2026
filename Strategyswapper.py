from Strategy import Strategy

class Strategyswapper:
   def swap_strategies_if_needed(self, strategy: Strategy) -> Strategy:
       if strategy.to_swap:
           return strategy.next_strategy
       else :
           return strategy