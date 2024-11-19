import 'package:flutter/material.dart';
import 'package:flutter_frontend/constants.dart';
import 'package:flutter_frontend/web/list_controller.dart';
import 'package:get/get.dart';

class WebHomePage extends StatelessWidget {
  WebHomePage({super.key});

  static const String WEB_HOME_PAGE_ROUTE = '/web';

  final ListController listController = Get.put(ListController());

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        leading: Icon(Icons.search),
        title: const Text('Smart Search'),
        backgroundColor: AppColor.primary,
      ),
      body: Center(
        child: Container(
          width: double.infinity,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Align(
                alignment: Alignment.topRight,
                child: Padding(
                  padding: EdgeInsets.only(right: 60.0),
                  child: OutlinedButton(
                    onPressed: () => {print("PDF upload")},
                    child: Text(
                      'Upload PDFs',
                      style: TextStyle(color: AppColor.secondary),
                    ),
                    style: ButtonStyle(backgroundColor:
                        MaterialStateProperty.resolveWith<Color>((states) {
                      if (states.contains(MaterialState.hovered)) {
                        return Colors.blue
                            .withOpacity(0.1); // Light blue on hover
                      }
                      return Colors
                          .transparent; // Default transparent background
                    })),
                  ),
                ),
              ),
              // Response window (ListView should take as much space as it needs)
              Obx(() {
                return Expanded(
                  child: Center(
                    child: ListView.builder(
                      shrinkWrap:
                          true, // This ensures ListView uses only as much space as needed
                      itemCount: listController.itemList.length,
                      itemBuilder: (context, index) {
                        return ListTile(
                          title: Text(listController.itemList[index]),
                        );
                      },
                    ),
                  ),
                );
              }),
              SizedBox(height: 20),
              Container(
                width: 600,
                child: TextField(
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
              SizedBox(height: 20),
              SizedBox(width: 500, child: SubmitButton())
            ],
          ),
        ),
      ),
    );
  }
}

// Define the fixed (no parameter) custom button widget
class SubmitButton extends StatelessWidget {
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
        // Action when the button is pressed
        print("Button Pressed");
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
