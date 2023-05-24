class Node:
    def __init__(self,item):
        self.item=item
        self.next=None
        
class LinkedList:
    def __init__(self):
       self.head=None
    def InsertionAtStart(self,newItem):
        NewNode = Node(newItem)
        NewNode.next = self.head
        self.head = NewNode

    def InsertionAtMiddle(self,MiddleNode,newItem):
        if MiddleNode is None:
            print("middle Node Is Abscent")
        else:
            newNode = Node(newItem)
            newNode.next = MiddleNode.next
            MiddleNode.next = newNode 
            
     
    def InsertionAtEnd(self,newItem):
        newNode = Node(newItem)
        if self.head == None:
            return newNode
        else:
            lastNode=self.head
            while(lastNode.next):
                lastNode = lastNode.next
            else:
                lastNode.next=newNode

                
Linked_List = LinkedList()
Linked_List.head = first = Node("Venkat")
first.next = second = Node("Vasu")
second.next = third = Node("Pavan")
third.next = fourth = Node("TRL")


Linked_List.InsertionAtStart("Srinivas")

Linked_List.InsertionAtMiddle(second,"SrinivasNaidu")

Linked_List.InsertionAtEnd("P.Srinivas")

while Linked_List.head:
    print(Linked_List.head.item)
    Linked_List.head = Linked_List.head.next
            
        
        
         
   