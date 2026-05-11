import WidgetKit
import SwiftUI

struct AngleEntry: TimelineEntry {
    let date: Date
    let angle: Double
}

struct AngleProvider: TimelineProvider {
    func placeholder(in context: Context) -> AngleEntry {
        AngleEntry(date: .now, angle: 0)
    }

    func getSnapshot(in context: Context, completion: @escaping (AngleEntry) -> Void) {
        completion(AngleEntry(date: .now, angle: 0))
    }

    func getTimeline(in context: Context, completion: @escaping (Timeline<AngleEntry>) -> Void) {
        let entry = AngleEntry(date: .now, angle: 0)
        let timeline = Timeline(entries: [entry], policy: .after(.now.addingTimeInterval(900)))
        completion(timeline)
    }
}

struct AngleComplicationView: View {
    let entry: AngleEntry

    @Environment(\.widgetFamily) var family

    var body: some View {
        switch family {
        case .accessoryCircular:
            ZStack {
                AccessoryWidgetBackground()
                VStack(spacing: 1) {
                    Image(systemName: "gauge")
                        .font(.system(size: 12, weight: .bold))
                    Text(String(format: "%.0f°", entry.angle))
                        .font(.system(size: 14, weight: .black, design: .rounded))
                        .monospacedDigit()
                }
            }
        case .accessoryCorner:
            Text(String(format: "%.0f°", entry.angle))
                .font(.system(size: 16, weight: .black, design: .rounded))
                .monospacedDigit()
                .widgetLabel {
                    Text("角度")
                }
        case .accessoryInline:
            Text("角度 \(String(format: "%.0f°", entry.angle))")
                .font(.system(size: 14, weight: .bold))
        case .accessoryRectangular:
            VStack(alignment: .leading, spacing: 2) {
                HStack(spacing: 4) {
                    Image(systemName: "gauge")
                        .font(.system(size: 10))
                    Text("職人ツール")
                        .font(.system(size: 10, weight: .bold))
                }
                Text(String(format: "%.1f°", entry.angle))
                    .font(.system(size: 22, weight: .black, design: .rounded))
                    .monospacedDigit()
                Text("ANGLE")
                    .font(.system(size: 9, weight: .bold, design: .monospaced))
                    .foregroundStyle(.secondary)
            }
        @unknown default:
            Text(String(format: "%.0f°", entry.angle))
        }
    }
}

@main
struct ShokuninComplications: Widget {
    let kind = "ShokuninAngle"

    var body: some WidgetConfiguration {
        StaticConfiguration(kind: kind, provider: AngleProvider()) { entry in
            AngleComplicationView(entry: entry)
                .containerBackground(.fill.tertiary, for: .widget)
        }
        .configurationDisplayName("職人ツール")
        .description("角度と傾きを表示")
        .supportedFamilies([
            .accessoryCircular,
            .accessoryCorner,
            .accessoryInline,
            .accessoryRectangular
        ])
    }
}
