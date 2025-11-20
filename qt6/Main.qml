import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Fusion
import QtQuick.Layouts
import QtQuick.Dialogs

ApplicationWindow {
    id: mainWindow
    width: 1200
    height: 800
    visible: true
    title: getText("bible_reader")
    color: "#f5f5f5"

    palette {
           window: "white"        // 窗口背景色
           windowText: "black"    // 窗口文字颜色
           base: "white"         // 输入控件背景色
           text: "black"         // 输入控件文字颜色
           button: "white"       // 按钮背景色
           buttonText: "black"   // 按钮文字颜色
       }

    // 语言管理器
    property string currentLanguage: "en"
    property var languages: ({
        "en": {
            "app_title": "Bible Reader",
            "language": "Language",
            "version": "Version",
            "volume": "Volume",
            "chapter": "Chapter",
            "verse_range": "Verse Range",
            "to": "to",
            "search": "Search",
            "case_sensitive": "Case Sensitive",
            "view_images": "View Images",
            "select_folder": "Select Folder",
            "select_image_folder": "Select Image Folder",
            "base_path": "Base Path",
            "available_folders": "Available Folders",
            "ok": "OK",
            "cancel": "Cancel",
            "manual_select": "Manual Select Folder",
            "warning": "Warning",
            "please_select_folder": "Please select a folder",
            "image_viewer": "Image Viewer",
            "current_folder": "Current Folder",
            "folder_location": "Folder Location",
            "filename": "Filename",
            "prev_image": "Previous",
            "next_image": "Next",
            "change_folder": "Change Folder",
            "no_images_found": "No images found in folder",
            "error": "Error",
            "folder_not_exist": "Folder does not exist"
        },
        "zh": {
            "app_title": "圣经阅读器",
            "language": "语言",
            "version": "版本",
            "volume": "卷",
            "chapter": "章",
            "verse_range": "节范围",
            "to": "至",
            "search": "搜索",
            "case_sensitive": "区分大小写",
            "view_images": "查看图片",
            "select_folder": "选择文件夹",
            "select_image_folder": "选择图片文件夹",
            "base_path": "基础路径",
            "available_folders": "可用的文件夹",
            "ok": "确定",
            "cancel": "取消",
            "manual_select": "手动选择文件夹",
            "warning": "警告",
            "please_select_folder": "请选择一个文件夹",
            "image_viewer": "图片查看器",
            "current_folder": "当前文件夹",
            "folder_location": "所在文件夹",
            "filename": "文件名",
            "prev_image": "上一张",
            "next_image": "下一张",
            "change_folder": "切换文件夹",
            "no_images_found": "文件夹中未找到图片文件",
            "error": "错误",
            "folder_not_exist": "文件夹不存在"
        }
    })

    function getText(key) {
        var langDict = languages[currentLanguage] || languages["en"];
        return langDict[key] || key;
    }

    function updateUIText() {
        // 这个函数会在语言改变时被调用，更新所有界面文本
        languageCombo.updateDisplayText();
    }

    // 主布局
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 10
        spacing: 10

        // 顶部控制面板
        Rectangle {
            id: controlPanel
            Layout.fillWidth: true
            height: 100
            color: "#ffffff"
            border.color: "#cccccc"
            border.width: 1
            radius: 4

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 5
                spacing: 5

                // 第一行控制项
                RowLayout {
                    Layout.fillWidth: true
                    spacing: 10

                    // 语言选择
                    Label {
                        text: getText("language") + ":"
                        font.pointSize: 10
                    }

                    ComboBox {
                        id: languageCombo
                        Layout.preferredWidth: 120
                        model: [
                            { code: "en", display: "English" },
                            { code: "zh", display: "中文" }
                        ]

                        property string currentLangCode: "en"

                        textRole: "display"

                        Component.onCompleted: {
                            currentIndex = indexOfValue("en")
                        }

                        function indexOfValue(langCode) {
                            for (var i = 0; i < model.length; i++) {
                                if (model[i].code === langCode) return i
                            }
                            return 0
                        }

                        function updateDisplayText() {
                            // 强制更新显示文本
                            var temp = currentIndex
                            currentIndex = -1
                            currentIndex = temp
                        }

                        onCurrentIndexChanged: {
                            if (currentIndex >= 0) {
                                var selectedLang = model[currentIndex].code
                                if (selectedLang !== mainWindow.currentLanguage) {
                                    mainWindow.currentLanguage = selectedLang
                                    mainWindow.updateUIText()
                                }
                            }
                        }
                    }

                    // 版本选择
                    Label {
                        text: getText("version") + ":"
                        font.pointSize: 10
                    }

                    ComboBox {
                        id: versionCombo
                        Layout.preferredWidth: 100
                        model: ["strjw", "NCB", "LCC", "TCB", "NIV"]
                        currentIndex: 0
                    }

                    // 卷选择
                    Label {
                        text: getText("volume") + ":"
                        font.pointSize: 10
                    }

                    ComboBox {
                        id: volumeCombo
                        Layout.preferredWidth: 150
                        model: ["1. Genesis", "2. Exodus", "3. Leviticus", "4. Numbers", "5. Deuteronomy"]
                        currentIndex: 0
                    }

                    // 章选择
                    Label {
                        text: getText("chapter") + ":"
                        font.pointSize: 10
                    }

                    ComboBox {
                        id: chapterCombo
                        Layout.preferredWidth: 80
                        model: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
                        currentIndex: 0
                    }

                    // 图片查看按钮 - 保持绿色样式
                    Button {
                        id: imageButton
                        text: getText("view_images")
                        Layout.alignment: Qt.AlignRight

                        background: Rectangle {
                            color: "#28a745"
                            radius: 4
                        }
                        contentItem: Text {
                            text: imageButton.text
                            color: "white"
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                            font.pointSize: 10
                        }

                        onClicked: imageViewerWindow.show()
                    }
                }

                // 第二行控制项
                RowLayout {
                    Layout.fillWidth: true
                    spacing: 10

                    // 节范围选择
                    Label {
                        text: getText("verse_range") + ":"
                        font.pointSize: 10
                    }

                    ComboBox {
                        id: verseStartCombo
                        Layout.preferredWidth: 80
                        model: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
                        currentIndex: 0
                    }

                    Label {
                        text: getText("to")
                        font.pointSize: 10
                    }

                    ComboBox {
                        id: verseEndCombo
                        Layout.preferredWidth: 80
                        model: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
                        currentIndex: 9
                    }

                    // 搜索框
                    Label {
                        text: getText("search") + ":"
                        font.pointSize: 10
                    }

                    TextField {
                        id: searchField
                        Layout.preferredWidth: 200
                        placeholderText: getText("search") + "..."
                    }

                    // 搜索按钮 - 保持蓝色样式
                    Button {
                        id: searchButton
                        text: getText("search")

                        background: Rectangle {
                            color: "#4a7abc"
                            radius: 4
                        }
                        contentItem: Text {
                            text: searchButton.text
                            color: "white"
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                            font.pointSize: 10
                        }
                    }

                    // 搜索选项
                    CheckBox {
                        id: caseCheckBox
                        text: getText("case_sensitive")
                        font.pointSize: 9
                    }
                }
            }
        }

        // 内容显示区域
        Rectangle {
            id: contentArea
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: "#ffffff"
            border.color: "#cccccc"
            border.width: 1
            radius: 4

            ScrollView {
                anchors.fill: parent
                anchors.margins: 10

                TextArea {
                    id: textDisplay
                    wrapMode: TextArea.Wrap
                    readOnly: true
                    font.pointSize: 12
                    color: "#333333"
                    text: {
                        if (currentLanguage === "en") {
                            return "Genesis 1:1-10\n\n1. In the beginning God created the heavens and the earth.\n2. Now the earth was formless and empty, darkness was over the surface of the deep, and the Spirit of God was hovering over the waters.\n3. And God said, \"Let there be light,\" and there was light.\n4. God saw that the light was good, and he separated the light from the darkness.\n5. God called the light \"day,\" and the darkness he called \"night.\" And there was evening, and there was morning—the first day."
                        } else {
                            return "创世纪 1:1-10\n\n1. 起初，神创造天地。\n2. 地是空虚混沌，渊面黑暗；神的灵运行在水面上。\n3. 神说：「要有光」，就有了光。\n4. 神看光是好的，就把光暗分开了。\n5. 神称光为「昼」，称暗为「夜」。有晚上，有早晨，这是头一日。"
                        }
                    }
                }
            }
        }
    }

    // 图片查看器窗口
    Window {
        id: imageViewerWindow
        width: 900
        height: 700
        title: getText("image_viewer")
        visible: false

        Rectangle {
            anchors.fill: parent
            color: "#ffffff"

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 10
                spacing: 10

                Label {
                    text: getText("image_viewer") + " - " + getText("no_images_found")
                    font.pointSize: 16
                    color: "#777777"
                    Layout.alignment: Qt.AlignCenter
                }

                // 选择文件夹按钮 - 保持蓝色样式
                Button {
                    text: getText("select_folder")
                    Layout.alignment: Qt.AlignCenter

                    background: Rectangle {
                        color: "#4a7abc"
                        radius: 4
                    }
                    contentItem: Text {
                        text: parent.text
                        color: "white"
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        font.pointSize: 10
                    }

                    onClicked: folderDialog.open()
                }
            }
        }
    }

    // 文件夹选择对话框
    Dialog {
        id: folderDialog
        title: getText("select_image_folder")
        modal: true
        standardButtons: Dialog.Ok | Dialog.Cancel

        ColumnLayout {
            width: parent.width
            spacing: 10

            Label {
                text: getText("available_folders") + ":"
                font.bold: true
            }

            ListView {
                Layout.preferredWidth: 300
                Layout.preferredHeight: 200
                model: ["Folder 1", "Folder 2", "Folder 3"]
                delegate: RadioDelegate {
                    text: modelData
                    width: ListView.view.width
                }
            }

            // 手动选择按钮 - 保持蓝色样式
            Button {
                text: getText("manual_select")
                Layout.alignment: Qt.AlignRight

                background: Rectangle {
                    color: "#4a7abc"
                    radius: 4
                }
                contentItem: Text {
                    text: parent.text
                    color: "white"
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    font.pointSize: 10
                }
            }
        }
    }
}
