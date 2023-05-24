class Node:
    def __init__(self,item):
        self.item = item
        self.next = None
        
class LinkedList:
    def __init__(self):
        self.head = None
    def InsertionInMiddle(self,middleNode,newItem):
        if middleNode is None:
            print("middle node Is abscent")
           
            
        else:
            newNode = Node(newItem)
            newNode.next = middleNode.next
            middleNode.next = newNode 
            
Linked_List = LinkedList()
Linked_List.head = First = Node("Venkat")
Second = Node("RLT")
Third = Node("TRL")
First.next = Second
Second.next = Third 

Linked_List.InsertionInMiddle(Second,"Srinivas")
 
while Linked_List.head:
     print(Linked_List.head.item)
     Linked_List.head = Linked_List.head.next
            