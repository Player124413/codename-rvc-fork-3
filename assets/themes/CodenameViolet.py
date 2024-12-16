from __future__ import annotations

from typing import Iterable
import gradio as gr

# gr.themes.builder()
from gradio.themes.base import Base
from gradio.themes.utils import colors, fonts, sizes
import time


class CodenameViolet(Base):
    def __init__(
        self,
        *,
        primary_hue: colors.Color | str = colors.neutral,
        secondary_hue: colors.Color | str = colors.neutral,
        neutral_hue: colors.Color | str = colors.neutral,
        spacing_size: sizes.Size | str = sizes.spacing_md,
        radius_size: sizes.Size | str = sizes.radius_md,
        text_size: sizes.Size | str = sizes.text_lg,
        font: fonts.Font | str | Iterable[fonts.Font | str] = (
            "Syne V",
            fonts.GoogleFont("Syne"),
            "ui-sans-serif",
            "system-ui",
        ),
        font_mono: fonts.Font | str | Iterable[fonts.Font | str] = (
            "ui-monospace",
            fonts.GoogleFont("Nunito Sans"),
        ),
    ):
        super().__init__(
            primary_hue=primary_hue,
            secondary_hue=secondary_hue,
            neutral_hue=neutral_hue,
            spacing_size=spacing_size,
            radius_size=radius_size,
            text_size=text_size,
            font=font,
            font_mono=font_mono,
        )
        self.name = ("CodenameViolet",)
        self.secondary_100 = ("#dbeafe",)
        self.secondary_200 = ("#bfdbfe",)
        self.secondary_300 = ("#93c5fd",)
        self.secondary_400 = ("#60a5fa",)
        self.secondary_50 = ("#eff6ff",)
        self.secondary_500 = ("#3b82f6",)
        self.secondary_600 = ("#2563eb",)
        self.secondary_700 = ("#1d4ed8",)
        self.secondary_800 = ("#1e40af",)
        self.secondary_900 = ("#1e3a8a",)
        self.secondary_950 = ("#1d3660",)

        super().set(
            # Blaise ( Colors modified by Codename;0 )
            background_fill_primary="#1f1a26",
            background_fill_primary_dark="#1f1a26",
            background_fill_secondary="#8381ae",
            background_fill_secondary_dark="#8381ae",
            block_background_fill="#2a2431",
            block_background_fill_dark="#2c2634",
            block_border_color="#4a4157",
            block_border_color_dark="#4a4157",
            block_border_width="1px",
            block_border_width_dark="1px",
            block_info_text_color="*body_text_color_subdued",
            block_info_text_color_dark="*body_text_color_subdued",
            block_info_text_size="*text_sm",
            block_info_text_weight="400",

            block_label_background_fill="*background_fill_primary",
            block_label_background_fill_dark="*background_fill_primary",

            block_label_border_color="*border_color_primary",
            block_label_border_color_dark="*border_color_primary",

            block_label_border_width="1px",
            block_label_border_width_dark="1px",
            block_label_margin="0",
            block_label_padding="*spacing_sm *spacing_lg",
            block_label_radius="calc(*radius_lg - 1px) 0 calc(*radius_lg - 1px) 0",
            block_label_right_radius="0 calc(*radius_lg - 1px) 0 calc(*radius_lg - 1px)",
            block_label_shadow="*block_shadow",
            block_label_text_color="*#1f1a26",
            block_label_text_color_dark="*#1f1a26",
            block_label_text_weight="400",
            block_padding="*spacing_xl",
            block_radius="*radius_md",
            block_shadow="none",
            block_shadow_dark="none",
            block_title_background_fill="#e4e3f4",
            block_title_background_fill_dark="#e4e3f4",
            block_title_border_color="none",
            block_title_border_color_dark="none",
            block_title_border_width="0px",
            block_title_padding="*block_label_padding",
            block_title_radius="*block_label_radius",
            block_title_text_color="#1f1a26",
            block_title_text_color_dark="#1f1a26",
            block_title_text_size="*text_md",
            block_title_text_weight="600",
            body_background_fill="#1f1a26",
            body_background_fill_dark="#1b1721",
            body_text_color="white",
            body_text_color_dark="white",
            body_text_color_subdued="*neutral_400",
            body_text_color_subdued_dark="*neutral_400",
            body_text_size="*text_md",
            body_text_weight="400",
            border_color_accent="*neutral_600",
            border_color_accent_dark="*neutral_600",
            border_color_primary="#4a4157",
            border_color_primary_dark="#4a4157",
            button_border_width="*input_border_width",
            button_border_width_dark="*input_border_width",
            button_cancel_background_fill="*button_secondary_background_fill",
            button_cancel_background_fill_dark="*button_secondary_background_fill",
            button_cancel_background_fill_hover="*button_cancel_background_fill",
            button_cancel_background_fill_hover_dark="*button_cancel_background_fill",
            button_cancel_border_color="*button_secondary_border_color",
            button_cancel_border_color_dark="*button_secondary_border_color",
            button_cancel_border_color_hover="*button_cancel_border_color",
            button_cancel_border_color_hover_dark="*button_cancel_border_color",
            button_cancel_text_color="#110F0F",
            button_cancel_text_color_dark="#110F0F",
            button_cancel_text_color_hover="#110F0F",
            button_cancel_text_color_hover_dark="#110F0F",
            button_large_padding="*spacing_lg calc(2 * *spacing_lg)",
            button_large_radius="*radius_lg",
            button_large_text_size="*text_lg",
            button_large_text_weight="600",
            button_primary_background_fill="*primary_600",
            button_primary_background_fill_dark="*primary_600",
            button_primary_background_fill_hover="*primary_500",
            button_primary_background_fill_hover_dark="*primary_500",
            button_primary_border_color="*primary_500",
            button_primary_border_color_dark="*primary_500",
            button_primary_border_color_hover="*primary_400",
            button_primary_border_color_hover_dark="*primary_400",
            button_primary_text_color="white",
            button_primary_text_color_dark="white",
            button_primary_text_color_hover="#110F0F",
            button_primary_text_color_hover_dark="#110F0F",
            button_secondary_background_fill="#423967",
            button_secondary_background_fill_dark="#423967",
            button_secondary_background_fill_hover="#a58fff",
            button_secondary_background_fill_hover_dark="#a58fff",
            button_secondary_border_color="#50465e",
            button_secondary_border_color_dark="#50465e",
            button_secondary_border_color_hover="*neutral_600",
            button_secondary_border_color_hover_dark="*neutral_600",
            button_secondary_text_color="white",
            button_secondary_text_color_dark="white",
            button_secondary_text_color_hover="*button_secondary_text_color",
            button_secondary_text_color_hover_dark="*button_secondary_text_color",
            button_small_padding="*spacing_sm calc(2 * *spacing_sm)",
            button_small_radius="*radius_lg",
            button_small_text_size="*text_md",
            button_small_text_weight="400",
            button_transition="0.3s ease all",

            checkbox_background_color="#594e69",
            checkbox_background_color_dark="#594e69",

            checkbox_background_color_focus="*checkbox_background_color",
            checkbox_background_color_focus_dark="*checkbox_background_color",
            checkbox_background_color_hover="*checkbox_background_color",
            checkbox_background_color_hover_dark="*checkbox_background_color",
            checkbox_background_color_selected="*#a58fff",
            checkbox_background_color_selected_dark="#a58fff",
            checkbox_border_color="#9581e6",
            checkbox_border_color_dark="#9581e6",
            checkbox_border_color_focus="*secondary_500",
            checkbox_border_color_focus_dark="*secondary_500", 
            checkbox_border_color_hover="*neutral_600",
            checkbox_border_color_hover_dark="*neutral_600",
            checkbox_border_color_selected="*secondary_600",
            checkbox_border_color_selected_dark="*secondary_600",
            checkbox_border_radius="*radius_sm",
            checkbox_border_width="*input_border_width",
            checkbox_border_width_dark="*input_border_width",
            checkbox_check="url(\"data:image/svg+xml,%3csvg viewBox='0 0 16 16' fill='white' xmlns='http://www.w3.org/2000/svg'%3e%3cpath d='M12.207 4.793a1 1 0 010 1.414l-5 5a1 1 0 01-1.414 0l-2-2a1 1 0 011.414-1.414L6.5 9.086l4.293-4.293a1 1 0 011.414 0z'/%3e%3c/svg%3e\")",
            checkbox_label_background_fill="transparent",
            checkbox_label_background_fill_dark="transparent",
            checkbox_label_background_fill_hover="transparent",
            checkbox_label_background_fill_hover_dark="transparent",
            checkbox_label_background_fill_selected="transparent",
            checkbox_label_background_fill_selected_dark="transparent",
            checkbox_label_border_color="transparent",
            checkbox_label_border_color_dark="transparent",
            checkbox_label_border_color_hover="transparent",
            checkbox_label_border_color_hover_dark="transparent",
            checkbox_label_border_width="transparent",
            checkbox_label_border_width_dark="transparent",
            checkbox_label_gap="*spacing_lg",
            checkbox_label_padding="*spacing_md calc(2 * *spacing_md)",
            checkbox_label_shadow="none",

            checkbox_label_text_color="*body_text_color",
            checkbox_label_text_color_dark="*body_text_color",

            checkbox_label_text_color_selected="*checkbox_label_text_color",
            checkbox_label_text_color_selected_dark="*checkbox_label_text_color",

            checkbox_label_text_size="*text_md",
            checkbox_label_text_weight="400",
            checkbox_shadow="*input_shadow",
            color_accent="#8a78d5",
            color_accent_soft="*primary_50",
            color_accent_soft_dark="*neutral_700",
            container_radius="*radius_xl",
            embed_radius="*radius_lg",
            error_background_fill="*background_fill_primary",
            error_background_fill_dark="*background_fill_primary",
            error_border_color="*border_color_primary",
            error_border_color_dark="*border_color_primary",
            error_border_width="1px",
            error_border_width_dark="1px",
            error_text_color="#ef4444",
            error_text_color_dark="#ef4444",
            form_gap_width="0px",
            input_background_fill="*neutral_900",
            input_background_fill_dark="*neutral_900",
            input_background_fill_focus="*secondary_600",
            input_background_fill_focus_dark="*secondary_600",
            input_background_fill_hover="*input_background_fill",
            input_background_fill_hover_dark="*input_background_fill",
            input_border_color="*neutral_700",
            input_border_color_dark="*neutral_700",
            input_border_color_focus="*secondary_600",
            input_border_color_focus_dark="*primary_600",
            input_border_color_hover="*input_border_color",
            input_border_color_hover_dark="*input_border_color",
            input_border_width="1px",
            input_border_width_dark="1px",
            input_padding="*spacing_xl",
            input_placeholder_color="*neutral_500",
            input_placeholder_color_dark="*neutral_500",
            input_radius="*radius_lg",
            input_shadow="none",
            input_shadow_dark="none",
            input_shadow_focus="*input_shadow",
            input_shadow_focus_dark="*input_shadow",
            input_text_size="*text_md",
            input_text_weight="400",
            layout_gap="*spacing_xxl",
            link_text_color="*secondary_500",
            link_text_color_active="#a58fff",
            link_text_color_active_dark="#a58fff",
            link_text_color_dark="*secondary_500",
            link_text_color_hover="*secondary_400",
            link_text_color_hover_dark="*secondary_400",
            link_text_color_visited="*secondary_600",
            link_text_color_visited_dark="*secondary_600",
            loader_color="*color_accent",
            loader_color_dark="*color_accent",
            panel_background_fill="*background_fill_secondary",
            panel_background_fill_dark="*background_fill_secondary",
            panel_border_color="*border_color_primary",
            panel_border_color_dark="*border_color_primary",
            panel_border_width="1px",
            panel_border_width_dark="1px",
            prose_header_text_weight="600",
            prose_text_size="*text_md",
            prose_text_weight="400",
            radio_circle="url(\"data:image/svg+xml,%3csvg viewBox='0 0 16 16' fill='white' xmlns='http://www.w3.org/2000/svg'%3e%3ccircle cx='8' cy='8' r='3'/%3e%3c/svg%3e\")",
            section_header_text_size="*text_md",
            section_header_text_weight="400",
            shadow_drop="rgba(0,0,0,0.05) 0px 1px 2px 0px",
            shadow_drop_lg="0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)",
            shadow_inset="rgba(0,0,0,0.05) 0px 2px 4px 0px inset",
            shadow_spread="3px",
            shadow_spread_dark="1px",
            slider_color="#9E9E9E",
            slider_color_dark="#9E9E9E",
            stat_background_fill="*primary_500",
            stat_background_fill_dark="*primary_500",
            table_border_color="*neutral_700",
            table_border_color_dark="*neutral_700",
            table_even_background_fill="*neutral_950",
            table_even_background_fill_dark="*neutral_950",
            table_odd_background_fill="*neutral_900",
            table_odd_background_fill_dark="*neutral_950",
            table_radius="*radius_lg",
            table_row_focus="*color_accent_soft",
            table_row_focus_dark="*color_accent_soft",
        )