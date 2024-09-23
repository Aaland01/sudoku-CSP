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
            # Added to support other ordering
            self.binary_constraints[(variable2, variable1)] = set()
            for value1 in self.domains[variable1]:
                for value2 in self.domains[variable2]:
                    if value1 != value2:
                        self.binary_constraints[(variable1, variable2)].add((value1, value2))
                        self.binary_constraints[(variable1, variable2)].add((value2, value1))
                        # Added to support other ordering
                        self.binary_constraints[(variable2, variable1)].add((value1, value2))
                        self.binary_constraints[(variable2, variable1)].add((value2, value1))
                        

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
            
        def select_unassigned_variable(assignment: dict[str, Any]):
            for variable in self.variables:
                if variable not in assignment:
                    return variable
            return None
                
        # domains: dict of [district, {possible colors}]
        # i.e. {'WA': {'green', 'red', 'blue'}, 'NT': {'green', 'red', 'blue'}, ... }
        #Any ordering is fine - sorted alphabetically just in case
        def order_domain_values(var):
            return self.domains[var]
        
        
        """
        Method for verifying that assigning a value to the current variable does not violate any 
        constraints with the values already assigned to other variables
        # --- Code is based on this:
            # To check if variable1=value1, variable2=value2 is in violation of a binary constraint:
            # if (
            #     (variable1, variable2) in self.binary_constraints and
            #     (value1, value2) not in self.binary_constraints[(variable1, variable2)]
            # ) or (
            #     (variable2, variable1) in self.binary_constraints and
            #     (value1, value2) not in self.binary_constraints[(variable2, variable1)]
            # ):
            #     Violates a binary constraint
        """
        def consistent(value, currentVariable, assignment):
            # Empty assignment dict implies no constraints violated
            if not assignment:
                return True
            constraints = self.binary_constraints
            # Check each variable in assignment
            for otherVariable in assignment:
                # Check possible first ordering:
                otherValue = assignment[otherVariable]
                variablePair = (currentVariable, otherVariable)
                if variablePair in constraints:
                    legalValuePairs = constraints[variablePair]
                    if (value, otherValue) not in legalValuePairs:
                        return False
                # Check possible other ordering --- however:
                #! Dont think this works, as the assignment says it does not store 
                #! the other order, only one order for each pair
                variablePair = (otherVariable, currentVariable)
                if variablePair in constraints:
                    legalValuePairs = constraints[variablePair]
                    if (otherValue, value) not in legalValuePairs:
                        return False
                # The two checks could be better implemented as a method as they are similar, 
                # only with different order. Leaving it be for now.
            # 
            return True
        
        def backtrack(assignment: dict[str, Any]):
            var = select_unassigned_variable(assignment)
            # Since select_unassigned_variable method basically is a completeness check, 
            # it returns None if no unassigned are left which is used to verify completeness.
            if var is None:
                return assignment
            for value in order_domain_values(var):
                if consistent(value, var, assignment):
                    assignment[var] = value
                    # Inferences are skipped per assignment description
                    result = backtrack(assignment)
                    if result is not None:
                        return result
                    assignment.pop(var)
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

    
    
    

    