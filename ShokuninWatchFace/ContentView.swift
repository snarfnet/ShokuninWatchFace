import SwiftUI

struct ContentView: View {
    @State private var selectedTool = 0

    var body: some View {
        TabView(selection: $selectedTool) {
            WatchAngleView()
                .tag(0)

            WatchLevelView()
                .tag(1)

            WatchCompassView()
                .tag(2)
        }
        .tabViewStyle(.verticalPage)
        .background(WatchWorkshopBackground())
    }
}

struct WatchWorkshopBackground: View {
    var body: some View {
        LinearGradient(
            colors: [
                Color(red: 0.018, green: 0.020, blue: 0.022),
                Color(red: 0.070, green: 0.076, blue: 0.074),
                Color(red: 0.100, green: 0.066, blue: 0.034)
            ],
            startPoint: .topLeading,
            endPoint: .bottomTrailing
        )
        .ignoresSafeArea()
    }
}
