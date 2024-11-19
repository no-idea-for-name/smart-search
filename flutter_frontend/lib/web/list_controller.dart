import 'package:get/get.dart';

class ListController extends GetxController {
  var itemList = <String>['test1', 'test2'].obs; // Reactive list of strings

  // Method to add an item to the list
  void addItem(String item) {
    itemList.add(item);
  }

  // Method to remove an item from the list
  void removeItem(String item) {
    itemList.remove(item);
  }
}
