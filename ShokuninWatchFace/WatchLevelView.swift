import SwiftUI

struct WatchLevelView: View {
    @StateObject private var motion = MotionManager()

    private var isLevel: Bool {
        abs(motion.pitch) < 2 && abs(motion.roll) < 2
    }

    private var bubbleOffset: CGSize {
        CGSize(
            width: max(-45, min(45, motion.roll * 2)),
            height: max(-45, min(45, -motion.pitch * 2))
        )
    }

    var body: some View {
        VStack(spacing: 8) {
            Text("水平器")
                .font(.system(size: 16, weight: .black, design: .rounded))
                .foregroundStyle(WatchPalette.title)

            ZStack {
                RoundedRectangle(cornerRadius: 22)
                    .fill(Color.black.opacity(0.42))
                    .overlay(
                        RoundedRectangle(cornerRadius: 22)
                            .stroke(WatchPalette.steel.opacity(0.28), lineWidth: 1)
                    )

                Circle()
                    .stroke(WatchPalette.amber.opacity(0.72), lineWidth: 3)
                    .frame(width: 102, height: 102)
                Circle()
                    .stroke(WatchPalette.steel.opacity(0.24), lineWidth: 1)
                    .frame(width: 56, height: 56)

                Rectangle()
                    .fill(WatchPalette.steel.opacity(0.28))
                    .frame(width: 1, height: 110)
                Rectangle()
                    .fill(WatchPalette.steel.opacity(0.28))
                    .frame(width: 110, height: 1)

                Circle()
                    .fill(isLevel ? WatchPalette.green : WatchPalette.red)
                    .frame(width: 28, height: 28)
                    .overlay(Circle().stroke(Color.white.opacity(0.52), lineWidth: 2))
                    .shadow(color: (isLevel ? WatchPalette.green : WatchPalette.red).opacity(0.62), radius: 10)
                    .offset(bubbleOffset)
                    .animation(.easeOut(duration: 0.15), value: bubbleOffset.width)
                    .animation(.easeOut(duration: 0.15), value: bubbleOffset.height)
            }
            .frame(width: 142, height: 142)

            Text(isLevel ? "LEVEL OK" : String(format: "%.1f°", motion.angle))
                .font(.system(size: 10, weight: .black, design: .monospaced))
                .foregroundColor(isLevel ? WatchPalette.green : WatchPalette.red)
        }
        .onAppear { motion.startUpdates() }
        .onDisappear { motion.stopUpdates() }
    }
}
