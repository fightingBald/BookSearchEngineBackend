"""

'.' matches any single character
'*' matches zero or more of the preceding element
'+' matches one or more of the preceding element
'?' matches zero or 1 of the preceding element
'|' matches the preceding element or following element
'()' groups a sequence of elements into one element
"""


def append_B_to_A(elem_A, elem_B):
    merge_callback = None

    _, last_appended_state = Ahoullman.State.append_B_to_A(
        elem_A, elem_B, merge_callback=merge_callback)

    return last_appended_state


class Ahoullman:
    def if_could_find_pattern(self, p, long_text: str)->bool:
        long_text_index_list = long_text.split(' ')
        for word in long_text_index_list:
            if self.match(p, word):
                return True
        return False

    def all_words_that_match_pattern(self, p, long_text: str)->list:
        long_text_index_list = long_text.split(' ')
        result = []
        for word in long_text_index_list:
            if self.match(p, word):
                result.append(word)
        return result
    def match(self, p, s):

        if isinstance(p, Ahoullman.NFA):
            nfa = p
        else:
            nfa = self.compile_pattern_to_nfa(p)

        for i, c in enumerate(s):

            nfa.step(c)

            if not len(nfa.cur_states):
                return False

        return nfa.contains_matching_state()

    def compile_pattern_to_nfa(self, p):
        _, nfa = self.__parse_current_pattern_pos(p, 0)
        return nfa

    def __parse_current_pattern_pos(self, p, start_pos):
        """Build a NFA for pattern p starting at position pos
        """
        last_elem = None
        cur_pos = start_pos

        nfa = self.NFA()

        while cur_pos < len(p):
            c = p[cur_pos]
            cur_elem = None

            if c == '(':
                if last_elem:
                    nfa.append_element(last_elem)
                cur_pos, sub_nfa = self.__parse_current_pattern_pos(p, cur_pos + 1)
                cur_pos += 1

                sub_nfa.start_state.char = Ahoullman.State.EMPTY_STATE
                sub_nfa.matching_state.char = Ahoullman.State.EMPTY_STATE

                last_elem = sub_nfa.elem()
                continue
            elif c == ')':
                break
            elif c == '|':
                if last_elem:
                    nfa.append_element(last_elem)
                    last_elem = None

                cur_pos, sub_nfa = self.__parse_current_pattern_pos(p, cur_pos + 1)

                nfa.or_nfa(sub_nfa)
                continue
            elif c == '*':

                cur_elem = self.State.create_element_star_state(last_elem)
                last_elem = None
            elif c == '+':

                cur_elem = self.State.create_element_plus_state(last_elem)
                last_elem = None
            elif c == '?':
                cur_elem = self.State.create_element_question_mark_state(
                    last_elem)
                last_elem = None
            else:
                if last_elem:
                    nfa.append_element(last_elem)

                last_elem = self.State.create_char_state(c)

            if cur_elem:
                nfa.append_element(cur_elem)
            cur_pos += 1

        if last_elem:
            nfa.append_element(last_elem)

        nfa.finalise_nfa()

        return cur_pos, nfa

    class State(object):
        START_STATE = '#S'
        MATCHING_STATE = '#M'
        EMPTY_STATE = '#E'

        @classmethod
        def get_state_description(cls, state):
            if state.char == cls.START_STATE:
                return 'Start'
            elif state.char == cls.MATCHING_STATE:
                return 'Matching'
            elif state.char == cls.EMPTY_STATE:
                return ''
            else:
                return state.char

        def __init__(self, char, in_states, out_states):
            self.char = char
            self.in_states = in_states
            self.out_states = out_states

        def is_start(self):
            return self.char == self.START_STATE

        def is_matching(self):
            return self.char == self.MATCHING_STATE

        def is_empty(self):
            return self.char == self.EMPTY_STATE

        def is_normal(self):
            return (not self.is_start() and
                    not self.is_matching() and
                    not self.is_empty())

        @classmethod
        def create_start_state(cls):
            new_state = cls(cls.START_STATE, set(), set())
            return new_state, new_state

        @classmethod
        def create_matching_state(cls):
            new_state = cls(cls.MATCHING_STATE, set(), set())
            return new_state, new_state

        @classmethod
        def create_empty_state(cls):
            new_state = cls(cls.EMPTY_STATE, set(), set())
            return new_state, new_state

        @classmethod
        def create_char_state(cls, char):
            new_state = cls(char, set(), set())
            return new_state, new_state

        @classmethod
        def append_B_to_A(cls, elem_A, elem_B, merge_callback=None):
            A = elem_A[1]
            B = elem_B[0]
            last_state = elem_B[1]
            if not ((A.is_start() and (
                    B.is_normal() or B.is_matching())) or (
                            A.is_normal() and (B.is_matching() or B.is_normal()))) and (
                    (len(A.out_states) == 0 and not A.is_normal()) or (len(B.in_states) == 0 and not B.is_normal())):
                if A.is_empty():
                    A.char = B.char

                A.out_states.discard(B)
                B.in_states.discard(A)

                A.out_states.update(B.out_states)

                for ous in B.out_states:
                    ous.in_states.discard(B)
                    ous.in_states.add(A)

                A.in_states.update(B.in_states)

                for ins in B.in_states:
                    ins.out_states.discard(B)
                    ins.out_states.add(A)

                if elem_B[0] == elem_B[1]:
                    last_state = A

                if merge_callback:
                    merge_callback()
            else:
                A.out_states.add(B)
                B.in_states.add(A)

            return elem_A[0], last_state

        @classmethod
        def create_element_star_state(cls, elem):
            facade_elem = cls.create_start_state()
            final_elem = cls.append_B_to_A(facade_elem, elem)
            facade_elem[1].char = cls.MATCHING_STATE
            final_elem = cls.append_B_to_A(final_elem, facade_elem)
            final_elem[1].char = cls.EMPTY_STATE
            return final_elem[1], final_elem[1]

        @classmethod
        def create_element_plus_state(cls, elem):
            if len(elem[0].out_states) == 1:
                os = elem[0].out_states.pop()
                tmp_elem = cls.append_B_to_A((elem[0], elem[0]), (os, os))
                if tmp_elem[1] != elem[0]:
                    elem[0].out_states.add(os)

            if len(elem[1].in_states) == 1:
                ins = elem[1].in_states.pop()
                tmp_elem = cls.append_B_to_A((ins, ins), (elem[1], elem[1]))
                if tmp_elem[1] == elem[1]:
                    elem[1].in_states.add(ins)
                else:
                    elem = (elem[0], tmp_elem[1])

            elem[1].out_states.add(elem[0])
            elem[0].in_states.add(elem[1])

            return elem

        @classmethod
        def create_element_question_mark_state(cls, elem):
            new_start_elem = cls.create_start_state()
            new_end_elem = cls.create_matching_state()
            final_elem = cls.append_B_to_A(new_start_elem, elem)
            final_elem = cls.append_B_to_A(final_elem, new_end_elem)
            final_elem = cls.append_B_to_A(
                (final_elem[0], final_elem[0]), (final_elem[1], final_elem[1]))
            final_elem[0].char = cls.EMPTY_STATE
            final_elem[1].char = cls.EMPTY_STATE
            return final_elem

    class NFA(object):
        def __init__(self):
            self.last_appended_state = Ahoullman.State.create_start_state()[1]
            self.start_state = self.last_appended_state
            self.matching_state = None
            self.cur_states = set()

        def elem(self):
            if self.matching_state:
                return self.start_state, self.matching_state
            else:
                return self.start_state, self.last_appended_state

        def reset(self):
            self.cur_states = {self.start_state}

        def contains_matching_state(self):
            if self.matching_state in self.cur_states:
                return True
            for cs in self.cur_states:
                if self.__contains_matching_state(cs):
                    return True
            return False

        def __contains_matching_state(self, state):
            if state == self.matching_state:
                return True
            else:
                if not state.is_normal():
                    for os in state.out_states:
                        if self.__contains_matching_state(os):
                            return True
                return False

        def step(self, char):
            # consume char then add next states
            states_remove = set()
            states_add = set()
            for cs in self.cur_states:
                states_remove.add(cs)
                states_add.update(self.__step_special_state(char, cs))
            self.cur_states.difference_update(states_remove)
            self.cur_states.update(states_add)

        def __step_special_state(self, char, state):
            states_add = set()
            if state.is_normal():
                if state.char == '.' or state.char == char:
                    states_add.update(state.out_states)
            else:
                for os in state.out_states:
                    states_add.update(self.__step_special_state(char, os))
            return states_add

        def append_element(self, elem):
            self.last_appended_state = append_B_to_A(
                (None, self.last_appended_state), elem)

        def or_nfa(self, nfa):
            A = self.start_state
            B = nfa.start_state
            if len(A.in_states) > 0 and len(B.in_states) > 0:
                # add [?] as the new start state and connect [?] to both [A]
                # and [B]
                A.char = Ahoullman.State.EMPTY_STATE
                B.char = Ahoullman.State.EMPTY_STATE
                new_start_elem = Ahoullman.State.create_char_state('T')
                append_B_to_A(new_start_elem, self.elem())
                append_B_to_A(new_start_elem, nfa.elem())
                new_start_elem[1].char = Ahoullman.State.START_STATE
                self.start_state = new_start_elem[1]
            elif len(A.in_states) > 0:
                # turn [B] to the new start state and append [A] to [B]
                A.char = Ahoullman.State.EMPTY_STATE
                append_B_to_A((None, B), self.elem())
                self.start_state = B
            else:
                # append [B] to [A] or merge [B] into [A]
                B.char = Ahoullman.State.EMPTY_STATE
                append_B_to_A((None, A), nfa.elem())

            A = self.last_appended_state
            B = nfa.matching_state
            if (len(A.out_states) > 0 or A.is_normal()) and len(B.out_states) > 0:
                # add [?] as the new matching state and connect both [A] and
                # [b] to [?]
                B.char = Ahoullman.State.EMPTY_STATE
                new_empty_elem = Ahoullman.State.create_char_state('T')
                self.last_appended_state = append_B_to_A(
                    (None, A), new_empty_elem)
                append_B_to_A((None, B), new_empty_elem)
                new_empty_elem[1].char = Ahoullman.State.EMPTY_STATE
            elif len(A.out_states) > 0 or A.is_normal():
                # append [B] to [A]
                B.char = Ahoullman.State.EMPTY_STATE
                self.last_appended_state = append_B_to_A(
                    (None, A), (B, B))
            else:
                # append [A] to [B] or merge [A] into [B]
                B.char = Ahoullman.State.EMPTY_STATE
                self.last_appended_state = append_B_to_A(
                    (None, B), (A, A))

        def finalise_nfa(self):

            new_matching_elem = Ahoullman.State.create_matching_state()
            self.matching_state = append_B_to_A(
                (None, self.last_appended_state), new_matching_elem)
            self.cur_states = {self.start_state}
            self.last_appended_state = None
