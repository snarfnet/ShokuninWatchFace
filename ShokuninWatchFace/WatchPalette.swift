import SwiftUI

enum WatchPalette {
    static let amber = Color(red: 1.000, green: 0.610, blue: 0.150)
    static let amberDeep = Color(red: 0.830, green: 0.360, blue: 0.060)
    static let steel = Color(red: 0.630, green: 0.675, blue: 0.670)
    static let paper = Color(red: 0.950, green: 0.900, blue: 0.780)
    static let green = Color(red: 0.200, green: 0.910, blue: 0.520)
    static let red = Color(red: 0.940, green: 0.180, blue: 0.120)
    static let iron = Color(red: 0.055, green: 0.061, blue: 0.064)

    static let title = LinearGradient(
        colors: [paper, amber],
        startPoint: .topLeading,
        endPoint: .bottomTrailing
    )
}
