class Node:
    def __init__(self,item):
        self.item = item
        self.next = None
        
class LinkedList:
    def __init__(self):
        self.head = None
    def InsertionAtEnd(self,newItem):
        newNode = Node(newItem)
        if self.head == None:
            return newNode
        else:
            newNode = Node(newItem)
            LastNode = self.head
            while(LastNode.next):
                LastNode = LastNode.next
            else:
                LastNode.next=newNode
                
Linked_List = LinkedList()

Linked_List.head = first = Node("Srinivas")
second = Node("Pavan")
third = Node("Madhu")

first.next = second
second.next = third

Linked_List.InsertionAtEnd("RLT")
while Linked_List.head:
    print(Linked_List.head.item)
    Linked_List.head = Linked_List.head.next