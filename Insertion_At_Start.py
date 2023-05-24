class Node:
    def __init__(self,item):
          self.item = item
          self.next = None
          
class LinkedList:
    def __init__(self):
        self.head = None
    def InsertionAtStart(self,newItem):
        NewNode = Node(newItem)
        NewNode.next = self.head
        self.head = NewNode
        
Linked_List =LinkedList()
Linked_List.head = First = Node("Raji")
Second = Node("Venkat")
Third = Node("Vasu")
First.next = Second
Second.next = Third
Linked_List.InsertionAtStart("Srinivas")
while Linked_List.head:
    print(Linked_List.head.item)
    Linked_List.head=Linked_List.head.next
    