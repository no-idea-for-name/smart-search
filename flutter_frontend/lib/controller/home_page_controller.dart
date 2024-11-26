import 'package:get/get.dart';

class HomeScreenController extends GetxController {
  var itemList = <String>[for (var i = 1; i <= 5; i++) 'test:$i'].obs;
 // Reactive list of strings

  // Method to add an item to the list
  void addItem(String item) {
    itemList.add(item);
  }

  // Method to remove an item from the list
  void removeItem(String item) {
    itemList.remove(item);
  }

  void submitRequest() {

  }

  deleteItem(int index) {
    itemList.removeAt(index);
  }
}
