import 'package:flutter/material.dart';
import 'package:flutter_frontend/constants.dart';
import 'package:flutter_frontend/controller/home_page_controller.dart';
import 'package:flutter_frontend/web/knowledge_manager_page.dart';
import 'package:get/get.dart';

class WebHomePage extends StatelessWidget {
  WebHomePage({super.key});

  static const String WEB_HOME_PAGE_ROUTE = '/web';

  final HomeScreenController homeScreenController =
      Get.put(HomeScreenController());

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        leading: Icon(Icons.search),
        title: const Text('Smart Search'),
        backgroundColor: AppColor.primary,
      ),
      body: Container(
        width: double.infinity,
        child: SingleChildScrollView(
          // Wrap everything in SingleChildScrollView
          child: Column(
            crossAxisAlignment:
                CrossAxisAlignment.center, // Align column items in the center
            mainAxisAlignment:
                MainAxisAlignment.center, // Center items in the column
            children: [
              Align(
                alignment: Alignment.topRight,
                child: Padding(
                  padding: EdgeInsets.only(right: 60.0),
                  child: OutlinedButton(
                    onPressed: () => {
                      Get.toNamed(KnowledgeManager.WEB_KOWLEDGE_MANAGER_ROUTE)
                    },
                    child: Text(
                      'Knowledge Manager',
                      style: TextStyle(color: AppColor.secondary),
                    ),
                    style: ButtonStyle(backgroundColor:
                        MaterialStateProperty.resolveWith<Color>((states) {
                      if (states.contains(MaterialState.hovered)) {
                        return Colors.grey
                            .withOpacity(0.1);
                      }
                      return Colors
                          .transparent;
                    })),
                  ),
                ),
              ),
              const SizedBox(
                height: 40,
              ),
              RequestListView(homeScreenController: homeScreenController),
              SizedBox(height: 20),
              Container(
                width: 600,
                child: const TextField(
                  minLines: 1,
                  maxLines: 14,
                  cursorColor: AppColor.secondary,
                  decoration: InputDecoration(
                    hintText: 'Search the incredible',
                    enabledBorder: OutlineInputBorder(
                        borderSide:
                            BorderSide(color: AppColor.secondary, width: 2.0)),
                    focusedBorder: OutlineInputBorder(
                      borderSide:
                          BorderSide(color: AppColor.secondary, width: 2.0),
                    ),
                    errorBorder: OutlineInputBorder(
                      borderSide: BorderSide(color: Colors.red, width: 2.0),
                    ),
                    focusedErrorBorder: OutlineInputBorder(
                      borderSide:
                          BorderSide(color: Colors.redAccent, width: 2.0),
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 20),
              SizedBox(width: 500, child: SubmitButton()),
              const SizedBox(height: 20),
            ],
          ),
        ),
      ),
    );
  }
}

class RequestListView extends StatelessWidget {
  const RequestListView({
    super.key,
    required this.homeScreenController,
  });

  final HomeScreenController homeScreenController;

  @override
  Widget build(BuildContext context) {
    return Obx(() {
      return Container(
        width: double.infinity,
        child: Center(
          // Center the ListView inside its container
          child: Container(
            width: 1000, // Set a specific width for centering
            child: ListView.builder(
              shrinkWrap: true,
              itemCount: homeScreenController.itemList.length,
              itemBuilder: (context, index) {
                return Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: Container(
                    decoration: BoxDecoration(
                        borderRadius: BorderRadius.circular(10),
                        border:
                            Border.all(color: AppColor.secondary, width: 2)),
                    child: ListTile(
                      leading: IconButton(
                          onPressed: () {
                            homeScreenController.deleteItem(index);
                          },
                          icon: Icon(Icons.delete)),
                      title: Container(
                          padding: EdgeInsets.all(10),
                          decoration: BoxDecoration(
                              border: Border.all(color: AppColor.secondary),
                              color: const Color.fromARGB(255, 218, 218, 218),
                              borderRadius: BorderRadius.circular(10)),
                          child: Text("Query: ")
                          //Text(homeScreenController.itemList[index])
                          ),
                      subtitle: Padding(
                          padding: EdgeInsets.only(top: 10),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [Text("test"), Text("data")])),
                    ),
                  ),
                );
              },
            ),
          ),
        ),
      );
    });
  }
}

// Define the fixed (no parameter) custom button widget
class SubmitButton extends StatelessWidget {
  final HomeScreenController homeScreenController =
      Get.find<HomeScreenController>();
  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      style: ButtonStyle(
        backgroundColor:
            MaterialStateProperty.all(AppColor.secondary), // Background color
        shape: MaterialStateProperty.all(
          RoundedRectangleBorder(
            borderRadius:
                BorderRadius.circular(16), // Border radius for rounded corners
          ),
        ),
      ),
      onPressed: () {
        homeScreenController.submitRequest();
      },
      child: Padding(
        padding: EdgeInsets.symmetric(
            vertical: 15, horizontal: 25), // Padding inside the button
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.send, color: Colors.white), // Icon inside button
            SizedBox(width: 10),
            Text(
              'Submit',
              style: TextStyle(color: Colors.white, fontSize: 18), // Text style
            ),
          ],
        ),
      ),
    );
  }
}
