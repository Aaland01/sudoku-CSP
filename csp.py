from typing import Any
from queue import Queue


class CSP:
    def __init__(
        self,
        variables: list[str],
        domains: dict[str, set],
        edges: list[tuple[str, str]],
    ):
        """Constructs a CSP instance with the given variables, domains and edges.
        
        Parameters
        ----------
        variables : list[str]
            The variables for the CSP
        domains : dict[str, set]
            The domains of the variables
        edges : list[tuple[str, str]]
            Pairs of variables that must not be assigned the same value
        """
        self.variables = variables
        self.domains = domains

        # Binary constraints as a dictionary mapping variable pairs to a set of value pairs.
        #
        # To check if variable1=value1, variable2=value2 is in violation of a binary constraint:
        # if (
        #     (variable1, variable2) in self.binary_constraints and
        #     (value1, value2) not in self.binary_constraints[(variable1, variable2)]
        # ) or (
        #     (variable2, variable1) in self.binary_constraints and
        #     (value1, value2) not in self.binary_constraints[(variable2, variable1)]
        # ):
        #     Violates a binary constraint
        self.binary_constraints: dict[tuple[str, str], set] = {}
        for variable1, variable2 in edges:
            self.binary_constraints[(variable1, variable2)] = set()
            for value1 in self.domains[variable1]:
                for value2 in self.domains[variable2]:
                    if value1 != value2:
                        self.binary_constraints[(variable1, variable2)].add((value1, value2))
                        self.binary_constraints[(variable1, variable2)].add((value2, value1))

    def ac_3(self) -> bool:
        """Performs AC-3 on the CSP.
        Meant to be run prior to calling backtracking_search() to reduce the search for some problems.
        
        Returns
        -------
        bool
            False if a domain becomes empty, otherwise True
        """
        # YOUR CODE HERE (and remove the assertion below)
        assert False, "Not implemented"

    def backtracking_search(self) -> None | dict[str, Any]:
        """Performs backtracking search on the CSP.
        
        Returns
        -------
        None | dict[str, Any]
            A solution if any exists, otherwise None
        """
        #! My code ----------------------------------------------------------------
        def select_unassigned_variable(self, assignment: dict[str, Any]):
            for variable in self.variables:
                if variable not in assignment:
                    return variable
            return None
                
        # domains: dict of [district, {possible colors}]
        # i.e. {'WA': {'green', 'red', 'blue'}, 'NT': {'green', 'red', 'blue'}, ... }
        #Any ordering is fine - 
        def order_domain_values(self, var):
            domainValues = self.domains[var]
            domainValues.sort()
            return domainValues
        
        
        """
        Verifying that assigning the value to the variable does not violate any 
        constraints with the values already assigned to other variables
        """
        def consistent(self, value, currentVariable, assignment):
            if not assignment:
                return True
            constraints = self.binary_constraints
            otherValue = assignment[otherVariable]
            for otherVariable in assignment:
                variablePair1 = (currentVariable, otherVariable)
                if variablePair1 in constraints:
                    legalValuePairs = constraints[variablePair1]
                    if (value, otherValue) in legalValuePairs:
                        return True
                variablePair2 = (otherVariable, currentVariable)
                if variablePair2 in constraints:
                    legalValuePairs = constraints[variablePair2]
                    if (otherValue, value) in legalValuePairs:
                        return True
            #! --- Above code is based on this:
            # To check if variable1=value1, variable2=value2 is in violation of a binary constraint:
            # if (
            #     (variable1, variable2) in self.binary_constraints and
            #     (value1, value2) not in self.binary_constraints[(variable1, variable2)]
            # ) or (
            #     (variable2, variable1) in self.binary_constraints and
            #     (value1, value2) not in self.binary_constraints[(variable2, variable1)]
            # ):
            #     Violates a binary constraint
            return False
        
        # Deprecated completenes-method, the same as select_unassigned_variable
        """
        def complete(self, assignment):
            for variable in self.variables:
                if variable not in assignment:
                    return False
            return True
        """
            
        def backtrack(assignment: dict[str, Any]):
            
            var = select_unassigned_variable(assignment)
            # Since select_unassigned_variable method basically is a completeness check, 
            # it returns None if no unassigned are left which is used to verify completeness.
            if var is None:
                return assignment
            for value in order_domain_values(var):
                if consistent(value, var, assignment):
                    assignment[value] = var
                    # Inferences are skipped per assignment description
                    result = backtrack(assignment)
                    if result is not None:
                        return result
                    assignment.pop(value)
            return None
            
        return backtrack({})
    
    """
	• INFERENCE: No inference needs to be performed during the backtracking search, 
        instead apply the AC-3 algorithm (figure 5.3 p171) prior to running the backtracking search. 
        This will reduce variable domain to one value each for simpler sudokus
    """


def alldiff(variables: list[str]) -> list[tuple[str, str]]:
    """Returns a list of edges interconnecting all of the input variables
    
    Parameters
    ----------
    variables : list[str]
        The variables that all must be different

    Returns
    -------
    list[tuple[str, str]]
        List of edges in the form (a, b)
    """
    return [(variables[i], variables[j]) for i in range(len(variables) - 1) for j in range(i + 1, len(variables))]

    
    
    

    