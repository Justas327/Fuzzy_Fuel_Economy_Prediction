import numpy as np


class FuzzyLogicTool:
    """
    TODO: Add centroid, MOM defuzzification methods
    """
    def __init__(self, membership_functions=None, rules=[]):
        self.memberships_processed = self.__process_membership_functions(membership_functions)
        self.memberships_functions = membership_functions

        self.rules = [self.__process_rule(rule) for rule in rules]

    def __get_fuzzy_values(self, test_case):
        results = []
        for i, attribute in enumerate(self.memberships_processed[:-1]):
            fuzzy_values = []
            for prop in attribute:
                fuzzy_values.append(self.triangle_f(test_case[i], prop))

            results.append(fuzzy_values)

        return results

    def compute(self, test_case):
        fuzzy_values = self.__get_fuzzy_values(test_case)
        implicated_results = self.__apply_implication_method(fuzzy_values)

        aggregated_results = self.__apply_aggregation_method(implicated_results)
        print(aggregated_results)

    def __apply_implication_method(self, fuzzy_values):
        rules_results = []

        for rule in self.rules:
            rules_results.append(FuzzyLogicTool.__get_rule_value(rule, fuzzy_values))

        return rules_results

    @staticmethod
    def __apply_aggregation_method(rules_output):
        rules_output = np.array(rules_output)
        unique_properties = {key: None for key in np.unique(rules_output[:, 1])}

        for output in rules_output[:, 1:]:
            if not unique_properties[output[0]]:
                unique_properties[output[0]] = output[1]
            else:
                unique_properties[output[0]] = max(unique_properties[output[0]], output[1])

        return [value for value in unique_properties.values()]

    @staticmethod
    def __get_rule_value(rule, fuzzy_values):
        result = []
        last_value = None
        reverse = False

        for index in rule:
            if last_value is not None:
                # Reverse operation
                if index == -1:
                    reverse = True
                    continue

                val = fuzzy_values[last_value][index]
                if reverse:
                    val = 1 - val
                result.append(val)

                last_value = None
            else:
                # Just adds and or operations indexes
                if index in [-3, -2]:
                    result.append(index)
                    continue
                if index == rule[-2]:
                    return FuzzyLogicTool.__parse_operations([rule[-2], rule[-1]] + result)
                last_value = index

        return None

    @staticmethod
    def __parse_operations(rule):
        result = rule[:2]

        for i, index in enumerate(rule[2:], start=2):
            if index == -2:
                result.append(min(rule[i - 1], rule[i + 1]))
            elif index == -3:
                result.append(max(rule[i - 1], rule[i + 1]))
            else:
                if rule[i - 1] not in [-3, -2] and (len(rule) == i + 1 or rule[i + 1] not in [-3, -2]):
                    result.append(index)

        return result

    @staticmethod
    def triangle_f(x, coords):
        if x < coords[0] or x > coords[2]:
            return 0
        elif coords[0] <= x <= coords[1]:
            return (x - coords[0]) / (coords[1] - coords[0])
        else:
            return (coords[2] - x) / (coords[2] - coords[1])

    @staticmethod
    def __process_membership_functions(functions):
        functions_matrix = []
        for key, val in functions.items():
            attributes = []
            for k, v in val.items():
                attributes.append(v)

            functions_matrix.append(attributes)

        return functions_matrix

    def __process_rule(self, rule):
        """
        Converts rule from human language to indexes
        Example:
        if weight is light and year is new then economy is high" -> [1, 0, -2, 2, 2, 3, 0]
        :param rule: rule string
        :return: index array
        """
        words = rule.split(' ')
        processed_rule = []

        # Process attributes names
        attribute_processed = False
        last_attribute = None
        for word in words:
            if word in ['if', 'is', 'then']:
                continue

            result = None

            try:
                if attribute_processed:
                    property_index = list(self.memberships_functions[last_attribute].keys()).index(word)
                    attribute_processed = False

                    result = property_index
                else:
                    index = list(self.memberships_functions.keys()).index(word)
                    result = index

                    attribute_processed = True
                    last_attribute = word
            except ValueError:
                result = word

            if word == 'and':
                result = -2
            if word == 'or':
                result = -3
            if word == 'not':
                result = -1

            processed_rule.append(result)

        return processed_rule

# Usage example below

#
# functions = {
#     "power": {
#         "low": [-175, 50, 185],
#         "medium": [125, 275, 425],
#         "high": [350, 500, 725]
#     },
#     "weight": {
#         "light": [-300, 700, 1300],
#         "medium": [1100, 1700, 2200],
#         "heavy": [2000, 2700, 3700]
#     },
#     "year": {
#         "old": [1945, 1970, 1985],
#         "normal": [1980, 1995, 2010],
#         "new": [2005, 2020, 2045]
#     },
#     "economy": {
#         "high": [-8, 3, 8.704],
#         "medium": [6.259, 12, 18],
#         "low": [16, 25, 36]
#     }
# }
#
# rules = ["if weight is light and year is new then economy is high",
#          "if power is low then economy is high",
#          "if power is medium and weight is not heavy then economy is medium",
#          "if power is medium and year is normal then economy is medium",
#          "if weight is heavy and year is not new then economy is low",
#          "if power is high then economy is low"]
#
# # rules = ["if weight is light and year is new then economy is high"]
#
# # input_data = [275, 1700, 1995]
# # input_data = [100, 1200, 2018]
# # input_data = [350, 2200, 1981]
# input_data = [126, 700, 2013]
#
# economy_prediction = FuzzyLogicTool(membership_functions=functions, rules=rules)
# economy_prediction.compute(input_data)