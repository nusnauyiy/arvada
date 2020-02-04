from lark import Lark

class Grammar():
    """
    Object representing a string-representation of a context-free grammar.
    This class is intended to be used with the Lark module.
    """
    def __init__(self, start):
        """
        Requires that terminals be wrapped in double quotes.
        Rules is a mapping of rule start name to Rule object.
        """
        # Add the first rule pointing a dummy start nonterminal to start
        start_rule = Rule('start')
        start_rule.add_body([start])
        self.rules = {'start':start_rule}

        # Optionally store a log that created the grammar
        self.log = None

        # Define cacheable values and their dirty bits
        self.cached_str = ""
        self.cached_str_valid = False
        self.cached_parser = None
        self.cached_parser_valid = False

    def add_rule(self, rule):
        self.cached_str_valid = False
        self.cached_parser_valid = False

        if rule.start in self.rules:
            saved_rule = self.rules[rule.start]
            for rule_body in rule.bodies:
                saved_rule.add_body(rule_body)
        else:
            self.rules[rule.start] = rule

    def parser(self):
        if self.cached_parser_valid:
            return self.cached_parser

        self.cached_parser = Lark(str(self))
        self.cached_parser_valid = True
        return self.cached_parser

    def __str__(self):
        if self.cached_str_valid:
            return self.cached_str

        self.cached_str = '\n'.join([str(rule) for rule in self.rules.values()])
        self.cached_str_valid = True
        return self.cached_str

class Rule():
    """
    Object representing the string-represenation of a rule of a CFG.
    There is always an associated grammar with every rule.
    This class is intended to be used with the Lark module.
    """
    def __init__(self, start):
        """
        Start must be a nonterminal.
        Each body is a sequence of terminals and nonterminals.
        If there are multiple bodies, they will be connected via the | op.
        """
        self.start = start
        self.bodies = []
        self.cached_str = ""
        self.cache_valid = False

    def add_body(self, body):
        self.cache_valid = False
        self.bodies.append(body)
        return self

    def __str__(self):
        if self.cache_valid:
            return self.cached_str

        self.cached_str = '%s: %s' % (self.start, self._body_str(self.bodies[0]))
        for i in range(1, len(self.bodies)):
            self.cached_str += '\n    | %s' % (self._body_str(self.bodies[i]))

        self.cache_valid = True
        return self.cached_str

    def _body_str(self, body):
        return ' '.join(body)

# Example grammar with nonterminals T1, T2 and terminals a, b
# grammar = Grammar('T1')
# grammar.add_rule(Rule('T1').add_body(['"a"', 'T2']).add_body(['"b"', 'T2']))
# grammar.add_rule(Rule('T2').add_body(['"b"']))
# parser = grammar.parser()
# print(parser.parse("ab").pretty())